import aiohttp

from aiohttp_proxy import ProxyConnector, ProxyType
from aiohttp.web import Application
from typing import Generator

from settings import PROXY_LIST


async def connect(app: Application) -> Generator:
    '''prox = PROXY_LIST.pop()
    connect_ = ProxyConnector(
        proxy_type=ProxyType.HTTP,
        host=prox.split(':')[0],
        port=prox.split(':')[1],
    )'''
    async with aiohttp.ClientSession() as session:
        app['sessions'] = session
        yield
