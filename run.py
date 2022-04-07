from aiohttp import web, hdrs

from views import HackerNewsProxy


app = web.Application()
app.router.add_route(hdrs.METH_ANY, '/{path:.*}', HackerNewsProxy.forward)


if __name__ == '__main__':
    web.run_app(app)

