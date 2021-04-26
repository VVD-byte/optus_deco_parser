import json
import logging

from aiohttp.web import View
from aiohttp import web

from pars_logic.parser import Parser


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def serialise(func):
    async def warp(*args, **kwargs):
        return web.Response(text=json.dumps(await func(*args, **kwargs)))
    return warp


class GetRequests(View):
    @serialise
    async def get(self):
        logger.info('Get requests')
        await Parser(self.request.app).get_all_tovar()


class GetCatalog(View):
    @serialise
    async def get(self):
        pass
