import asyncio
import random
import logging
import nest_asyncio
import re

from aiohttp.web import Application
from bs4 import BeautifulSoup

from pars_logic.utils import XmlWriter

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, app: Application):
        self.app = app
        self.n = 0
        logger.info('__init__ Parser')

    async def get_all_tovar(self):
        url = 'http://opusdeco.ru/catalog/wallpapers/?PAGE_CNT=500'
        bs = await self.get_soup(url)
        count_page = await self.get_page(bs)
        courutines = [self.get_tovar_for_page(f'{url}&PAGEN_3={i}')
                      for i in range(1, 4)]
                    # for i in range(2, count_page + 1)]
        result = self.app['loop'].run_until_complete(asyncio.gather(*courutines))
        result = [j for i in result for j in i]
        courutines = [self.check_tovar(i['Наличие'], i['Артикул'])
                      for i in result]
        result_ = self.app['loop'].run_until_complete(asyncio.gather(*courutines))
        for id_, i in enumerate(result_):
            result[id_]['Наличие'] = i
        XmlWriter(result).main()
        print(result)

    async def get_tovar_for_page(self, url):
        bs = await self.get_soup(url)
        try:
            dat = []
            for i in bs.find_all('div', {'class': 'bx_catalog_item double'}):
                for j in bs.select('strong'):
                    j.extract()
                dat_tovar = i.find('div', {'class': 'bx_catalog_item_articul'}).getText().split('\n')
                dat_tovar = [i for i in dat_tovar if i != '']
                dat.append({})
                dat[-1]['Бренд'] = dat_tovar[0].replace('  ', '')
                dat[-1]['Артикул'] = dat_tovar[1].replace('  ', '')
                dat[-1]['Наличие'] = re.findall(r'.{8}-.{4}-.{4}-.{4}-.{12}', i.find('a').get('style'))[0]
                if dat[-1]['Бренд'] in ['070209', '070193', '070186']:
                    print(dat[-1]['Наличие'])
        except Exception as e:
            print(e)
        return dat

    async def check_tovar(self, id_: str, name):
        """{
                    text[4]: text[12].replace('\xa0', ''),
                    text[5]: text[13].replace('\xa0', ''),
                    text[6]: text[14].replace('\xa0', ''),
                    text[7]: text[15].replace('\xa0', ''),
                }"""
        url = 'https://opusdeco.ru/getqnty.php'
        bs = await self.post_soup(url, {'extid': id_})
        if bs.getText() == '':
            return 'Товара нет на складе'
        text = bs.getText().split('\n')
        text = [i for i in text if i != '']
        if 'Ожидаем' in text[0]:
            return 'Ожидаем поступления на склад'
        try:
            if text[text.index('Свободно') + 2].replace('\xa0', '') == '':
                print(f"{text} - {text[text.index('Свободно') + 4]} - {name}")
                return text[text.index('Свободно') + 4].replace('\xa0', '')
            return text[text.index('Свободно') + 2].replace('\xa0', '')
        except:
            print(1)

    async def get_page(self, bs: BeautifulSoup) -> int:
        return int(bs.find('div', {'class': 'modern-page-navigation'}).find_all('a')[-3].getText())

    async def get_soup(self, url: str) -> BeautifulSoup:
        async with self.app['sessions'].get(url, ssl=False) as response:
            dat = await response.read()
            logger.info(f'Get Tovar For Url {url} - {response.status}')
            return BeautifulSoup(dat, 'lxml')

    async def post_soup(self, url: str, data: dict) -> BeautifulSoup:
        async with self.app['sessions'].post(url, data=data, ssl=False) as response:
            logger.info('POST REQUESTS')
            dat = await response.read()
            self.n += 1
            logger.info(f'POST Tovar For Url {url} - {response.status} - {self.n}')
            return BeautifulSoup(dat, 'lxml')

