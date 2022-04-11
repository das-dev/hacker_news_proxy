import mimetypes
from urllib.parse import urljoin

from aiohttp import web, hdrs, ClientSession
from multidict import MultiDict

from services import patch_html
from settings import HACKER_NEWS_HOST


async def proxify_request(request: web.Request) -> web.Response:
    async with ClientSession() as session:
        async with session.request(
                request.method,
                url=urljoin(HACKER_NEWS_HOST, request.path_qs),
                data=await request.post(),
                headers=request.headers
        ) as response:
            content = await response.content.read()
            content_type = response.headers.get(hdrs.CONTENT_TYPE, '')
            if mimetypes.types_map.get('.html', '') in content_type:
                content = patch_html(content, HACKER_NEWS_HOST)
            headers = MultiDict({hdrs.CONTENT_TYPE: content_type})
            return web.Response(body=content, headers=headers)
