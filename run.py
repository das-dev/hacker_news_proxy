import mimetypes
from urllib.parse import urljoin

from aiohttp import web, hdrs, ClientSession

from services import patch_html


class HackerNewsProxy(web.View):
    HACKER_NEWS_HOST = 'https://news.ycombinator.com/'

    def make_url(self) -> str:
        return urljoin(self.HACKER_NEWS_HOST, self.request.path_qs)

    @classmethod
    def _make_response(cls, content: bin, content_type: str) -> web.Response:
        if mimetypes.types_map.get('.html', '') in content_type:
            content = patch_html(content, cls.HACKER_NEWS_HOST)
        headers = {hdrs.CONTENT_TYPE: content_type}
        return web.Response(body=content, headers=headers)

    async def get(self) -> web.Response:
        async with ClientSession() as session:
            async with session.get(self.make_url(),
                                   headers=self.request.headers) as response:
                origin_content_type = response.headers.get(hdrs.CONTENT_TYPE)
                origin_content = await response.content.read()
        return self._make_response(origin_content, origin_content_type)

    async def post(self) -> web.Response:
        async with ClientSession() as session:
            async with session.post(self.make_url(),
                                    data=await self.request.post(),
                                    headers=self.request.headers) as response:
                origin_content_type = response.headers.get(hdrs.CONTENT_TYPE)
                origin_content = await response.content.read()
        return self._make_response(origin_content, origin_content_type)


app = web.Application()
app.router.add_view('/{path:.*}', HackerNewsProxy)

if __name__ == '__main__':
    web.run_app(app)
