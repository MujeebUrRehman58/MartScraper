import requests
from datetime import datetime as dt
import re

from bs4 import BeautifulSoup as BS

from src.db import Product
from src.db import ProductHistory
from src.scripts.queries import create_product
from src.scripts.queries import create_product_history
from src.scripts.queries import find_product_by_name_and_company


def disco_scraper(company_id):
    # this url will change for other categories
    url = "https://www.disco.com.uy/buscapagina?sc=4&fq=C%3a%2f412%2f&" \
          "PS=20&sl=994d903c-157c-4807-b8a3-ae3c5e511a30&cc=1&sm=0&PageNumber={}"
    api = "https://www.disco.com.uy/api/catalog_system/pub/products/search/?&fq=productId:{}"
    while True:
        page_number = 1
        page = requests.get(url.format(page_number))
        products = BS(page.content, 'html.parser').select('.Product')
        if not products:
            break
        for p in products:
            res = requests.get(api.format(p['productid'])).json()[0]
            name = res['productName']
            price = res['items'][0]['sellers'][0]['commertialOffer']['ListPrice']
            currency = '$'
            date_time_scrap = dt.utcnow()
            product_id = find_product_by_name_and_company(name, company_id) 
            if product_id:
                create_product_history(ProductHistory(
                    price=price, currency=currency, date_time_scrap=date_time_scrap), product_id
                )
            else:
                image = res['items'][0]['images'][0]['imageUrl']
                url_img = re.sub(r"([0-9]+(?=/.*.jpg))(/.*.jpg)", r"\1-1000-1000\2", image)
                thumb_url_img = re.sub(r"([0-9]+(?=/.*.jpg))(/.*.jpg)", r"\1-250-250\2", image)
                category_name = res['categories'][1]
                sub_category_name = res['categories'][0]
                url_product = res['link']
                create_product(Product(
                    name=name, price=price, currency=currency, date_time_scrap=date_time_scrap,
                    url_img=url_img, thumb_url_img=thumb_url_img, category_name=category_name,
                    sub_category_name=sub_category_name, url_product=url_product), company_id)

        page_number += 1


def tata_scraper(company_id=2):
    api = "https://www.tata.com.uy/api/catalog_system/pub/products/search/" \
          "almacen/desayuno?O=OrderByTopSaleDESC&_from={}&_to={}&ft&sc=4"
    while True:
        page_number = 1
        _to = page_number*50-50
        _from = page_number*50-1
        products = requests.get(api.format(_to, _from)).json()
        if not products:
            break
        for p in products:
            name = p['productName']
            price = p['items'][0]['sellers'][0]['commertialOffer']['ListPrice']
            currency = '$'
            date_time_scrap = dt.utcnow()
            product_id = find_product_by_name_and_company(name, company_id)
            if product_id:
                create_product_history(ProductHistory(
                    price=price, currency=currency, date_time_scrap=date_time_scrap), product_id
                )
            else:
                image = p['items'][0]['images'][0]['imageUrl']
                url_img = re.sub(r"([0-9]+(?=/.*.jpg))(/.*.jpg)", r"\1-1000-1000\2", image)
                thumb_url_img = re.sub(r"([0-9]+(?=/.*.jpg))(/.*.jpg)", r"\1-250-250\2", image)
                category_name = p['categories'][1]
                sub_category_name = p['categories'][0]
                url_product = p['link']
                create_product(Product(
                    name=name, price=price, currency=currency, date_time_scrap=date_time_scrap,
                    url_img=url_img, thumb_url_img=thumb_url_img, category_name=category_name,
                    sub_category_name=sub_category_name, url_product=url_product), company_id)

        page_number += 1


tata_scraper()
