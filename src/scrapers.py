import requests
from datetime import datetime as dt
import re
import pathlib
import json
import traceback

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.db import Product
from src.db import ProductHistory
from src.scripts.queries import create_product
from src.scripts.queries import create_product_history
from src.scripts.queries import find_product_by_external_id_and_company


chrome_options = Options()
chrome_options.add_argument("--headless")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
session = requests.session()
session.headers = {'User-Agent': user_agent}


def get_value_by_path(data, path):
    val = data
    for p in json.loads(path.replace('\'', "\"")):
        if p.isdigit():
            p = int(p)
        val = val[p]
    return val


def extract_category(cat, index, get_text=False):
    try:
        val = cat[index]
        if get_text:
            val = val.get_text()
    except:
        val = ''
    return val


def log_message(message):
    print(f'{dt.now()} {message}')


def transform_json_data(data, config):
    try:
        category = [i for i in get_value_by_path(data, config.category_name_path).split('/') if i]
        category_name = extract_category(category, 0)
        log_message(f'Begin {category_name} for company {config.company_id}')
        url_product = get_value_by_path(data, config.product_url_path)
        price = get_value_by_path(data, config.product_price_path)
        external_product_id = int(get_value_by_path(data, config.external_product_id_path))
        currency = '$'
        date_time_scrap = dt.utcnow()
        name = get_value_by_path(data, config.product_name_path)
        product_id = find_product_by_external_id_and_company(external_product_id, config.company_id)
        if product_id:
            print(f'Product with name \'{name}\', external id {external_product_id}'
                  f' and company id {config.company_id} already exists')
            create_product_history(ProductHistory(
                price=price, currency=currency, date_time_scrap=date_time_scrap), product_id
            )
        else:
            image = get_value_by_path(data, config.product_thumb_img_path)
            url_img = re.sub(r"([0-9]+(?=/.*.jpg))(/.*.jpg)", r"\1-1000-1000\2", image)
            thumb_url_img = re.sub(r"([0-9]+(?=/.*.jpg))(/.*.jpg)", r"\1-250-250\2", image)
            sub_category_name = extract_category(category, 1)
            sub_sub_category_name = extract_category(category, 2)
            create_product(Product(
                name=name, price=price, currency=currency, date_time_scrap=date_time_scrap,
                external_product_id=external_product_id, url_img=url_img, thumb_url_img=thumb_url_img,
                category_name=category_name, sub_category_name=sub_category_name,
                sub_sub_category_name=sub_sub_category_name, url_product=url_product), config.company_id)
        log_message(f'End {category_name} for company {config.company_id}')
    except:
        print(f'Error\n{traceback.format_exc()}\nFor data:\n{data}')


def api_bs_scraper(config):
    page_number = 1
    while True:
        page = requests.get(config.url.format(page_number))
        products = BS(page.content, 'html.parser').select(config.product_items_path)
        if not products:
            break
        for p in products:
            res = requests.get(config.api.format(p['productid']))
            if res.status_code == 200:
                res_json = res.json()
                if res_json and isinstance(res_json, list) and isinstance(res_json[0], dict):
                    transform_json_data(res_json[0], config)
        page_number += 1


def api_scraper(config):
    page_number = 1
    while True:
        _from = page_number*50-50
        _to = page_number * 50 - 1
        products = []
        res = requests.get(config.api.format(_from, _to))
        if res.status_code == 200:
            res_json = res.json()
            products = res_json if isinstance(res_json, list) else products
        if not products:
            break
        for p in products:
            transform_json_data(p, config)
        page_number += 1


def selenium_scraper(config):
    driver = webdriver.Chrome(f'{pathlib.Path(__file__).parent.absolute()}/chromedriver/chromedriver',
                              chrome_options=chrome_options)
    driver.set_window_size(1804, 1096)
    page_number = 0
    while True:
        driver.get(config.url.format(page_number))
        products = driver.find_elements_by_css_selector(config.product_items_path)
        if not products:
            break
        category = driver.find_elements_by_css_selector(config.category_name_path)[1].text
        for p in products:
            log_message(f'Begin {category} for company {config.company_id}')
            url_product = p.find_element_by_css_selector(config.product_url_path).get_attribute('href')
            external_product_id = int(url_product.split('producto?')[1].split(',')[0])
            price = p.find_element_by_css_selector(config.product_price_path).text
            currency = re.findall(r'[^ 0-9]+', price)[0]
            price = int(''.join(re.findall(r'[0-9]', price)))
            date_time_scrap = dt.utcnow()
            name = p.find_element_by_css_selector(config.product_name_path).text
            product_id = find_product_by_external_id_and_company(external_product_id, config.company_id)
            if product_id:
                print(f'Product with name \'{name}\', external id {external_product_id}'
                      f' and company id {config.company_id} already exists')
                create_product_history(ProductHistory(
                    price=price, currency=currency, date_time_scrap=date_time_scrap), product_id
                )
            else:
                thumb_url_img = p.find_element_by_css_selector(config.product_thumb_img_path).get_attribute('src')
                url_img = re.sub('/small/', '/large/', thumb_url_img)
                res = session.get(url_product)
                res = BS(res.content, 'html.parser')
                crumbs = res.select(config.category_name_path)
                category_name = extract_category(crumbs, 1, get_text=True)
                sub_category_name = extract_category(crumbs, 2, get_text=True)
                sub_sub_category_name = extract_category(crumbs, 3, get_text=True)
                create_product(Product(
                    name=name, price=price, currency=currency, date_time_scrap=date_time_scrap,
                    external_product_id=external_product_id, url_img=url_img, thumb_url_img=thumb_url_img,
                    category_name=category_name, sub_category_name=sub_category_name,
                    sub_sub_category_name=sub_sub_category_name, url_product=url_product), config.company_id)
            log_message(f'Begin {category} for company {config.company_id}')
        page_number += 1
    driver.close()

