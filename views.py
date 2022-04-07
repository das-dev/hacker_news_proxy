import mimetypes
from urllib.parse import urljoin

import httpx
from aiohttp import web, hdrs

from content_handler import HTMLHandler


class HackerNewsProxy:
    HACKER_NEWS_HOST = 'https://news.ycombinator.com/'

    def __init__(self, request):
        self.request = request
        self.url = self.make_url()

    def make_url(self):
        return urljoin(self.HACKER_NEWS_HOST, self.request.path_qs)

    @classmethod
    def forward(cls, request):
        proxy = HackerNewsProxy(request)
        return proxy.make_request()

    def make_request(self):
        method = getattr(self, self.request.method.lower())
        return method()

    def get(self):
        origin_response = httpx.get(self.make_url())
        origin_content = origin_response.content
        origin_content_type = origin_response.headers.get(hdrs.CONTENT_TYPE)
        if mimetypes.types_map.get('.html', '') in origin_content_type:
            origin_content = HTMLHandler(origin_content).handle()
        headers = {hdrs.CONTENT_TYPE: origin_content_type}
        return web.Response(body=origin_content, headers=headers)
