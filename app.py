from aiohttp import web, hdrs

from views import proxify_request


app = web.Application()
app.router.add_route(hdrs.METH_ANY, '/{path:.*}', proxify_request)

if __name__ == '__main__':
    web.run_app(app)
