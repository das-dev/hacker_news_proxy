import mimetypes
from urllib.parse import urljoin

from aiohttp import web, hdrs, ClientSession
from multidict import MultiDict

from services import patch_html
from settings import HACKER_NEWS_HOST


class HackerNewsProxy(web.View):
    async def get(self) -> web.Response:
        async with ClientSession() as session:
            async with session.get(self._make_url(),
                                   headers=self.request.headers) as response:
                origin_content_type = response.headers.get(hdrs.CONTENT_TYPE, '')
                origin_content = await response.content.read()
        return self._make_response(origin_content, origin_content_type)

    async def post(self) -> web.Response:
        async with ClientSession() as session:
            async with session.post(self._make_url(),
                                    data=await self.request.post(),
                                    headers=self.request.headers) as response:
                origin_content_type = response.headers.get(hdrs.CONTENT_TYPE, '')
                origin_content = await response.content.read()
        return self._make_response(origin_content, origin_content_type)

    def _make_url(self) -> str:
        return urljoin(HACKER_NEWS_HOST, self.request.path_qs)

    @classmethod
    def _make_response(cls, content: bytes, content_type: str) -> web.Response:
        if mimetypes.types_map.get('.html', '') in content_type:
            content = patch_html(content, HACKER_NEWS_HOST)
        headers = MultiDict({hdrs.CONTENT_TYPE: content_type})
        return web.Response(body=content, headers=headers)
