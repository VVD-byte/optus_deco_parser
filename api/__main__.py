import logging
import os
import asyncio

from aiohttp import web
from api.views import GetRequests

from api.signals import connect
from settings import PROXY_LIST


loop = asyncio.get_event_loop()


def main():
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app['loop'] = loop
    app.router.add_view('/', GetRequests)
    app.cleanup_ctx.append(connect)
    web.run_app(app)


if __name__ == '__main__':
    main()
