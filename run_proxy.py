import mimetypes
from urllib.parse import urljoin

import httpx
import lxml.html
from aiohttp import web, hdrs

HACKER_NEWS_HOST = 'https://news.ycombinator.com/'


def parse_html(html):
    tree = lxml.html.fromstring(html)
    return lxml.html.tostring(tree, encoding='unicode')


async def fetch_html(request):
    url = urljoin(HACKER_NEWS_HOST, request.path_qs)
    html = httpx.get(url).text
    content = parse_html(html)
    headers = {hdrs.CONTENT_TYPE: mimetypes.types_map['.html']}
    return web.Response(text=content, headers=headers)


async def fetch_favicon(request):
    url = urljoin(HACKER_NEWS_HOST, request.path_qs)
    content = httpx.get(url).content
    return web.Response(body=content)


app = web.Application()
app.router.add_route(hdrs.METH_GET, '/favicon.ico', fetch_favicon)
app.router.add_route(hdrs.METH_ANY, '/{path:.*}', fetch_html)


if __name__ == '__main__':
    web.run_app(app)

