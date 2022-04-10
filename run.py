from aiohttp import web

from views import HackerNewsProxy


app = web.Application()
app.router.add_view('/{path:.*}', HackerNewsProxy)

if __name__ == '__main__':
    web.run_app(app, port=80)
