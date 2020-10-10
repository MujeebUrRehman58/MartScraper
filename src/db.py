import mysql.connector as conn

from src import config

db = conn.connect(
    host=config.HOST,
    user=config.USER,
    password=config.PASSWORD,
    database=config.DATABASE
)
db_cursor = db.cursor()


# models
class Company(object):
    def __init__(self, company_name):
        self.company_name = company_name


class Product:
    def __init__(self, name, price, currency, date_time_scrap, url_img=None, thumb_url_img=None,
                 category_name=None, sub_category_name=None, url_product=None):
        self.name = name
        self.price = price
        self.currency = currency
        self.date_time_scrap = date_time_scrap
        self.url_img = url_img
        self.thumb_url_img = thumb_url_img
        self.category_name = category_name
        self.sub_category_name = sub_category_name
        self.url_product = url_product


class ProductHistory:
    def __init__(self, price, currency, date_time_scrap):
        self.price = price
        self.currency = currency
        self.date_time_scrap = date_time_scrap
