from enum import Enum
from collections import namedtuple

from src.scrapers import selenium_scraper
from src.scrapers import api_scraper
from src.scrapers import api_bs_scraper


class CompanyNameEnum(Enum):
    TIENDAINGLESA = 'TiendaInglesa'
    TATA = 'Tata'
    DISCO = 'Disco'
    GEANT = 'Geant'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


ScrapWith = namedtuple('ScrapWith', ['name', 'func'])


class ScrapWithEnum(Enum):
    SELENIUM = ScrapWith('SELENIUM', selenium_scraper)
    API = ScrapWith('API', api_scraper)
    API_BS = ScrapWith('API_BS', api_bs_scraper)

    @classmethod
    def filter_by_name(cls, name):
        return [i for i in cls if i.name == name][0]


class TablesEnum(Enum):
    HISTORY = 'ProductHistory'
    PRODUCT = 'Product'
    SCRAP_CONFIGURATOR = 'ScrapConfigurator'
    COMPANY = 'Company'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))