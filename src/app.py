# scraper code goes here
from datetime import datetime, timedelta

from src.scripts.queries import create_company
from src.scripts.queries import create_product
from src.scripts.queries import create_product_history
from src.db import Company
from src.db import Product
from src.db import ProductHistory

# dummy_data
company = Company(company_name='TiendaInglesa')
c_id = create_company(company)

product = Product(name='product1', price=10.5, currency='Dollar',
                  date_time_scrap=datetime.now(), url_img='https://www.google.com/',
                  thumb_url_img='https://www.google.com/', category_name='Almacen',
                  sub_category_name='sub sub', url_product='https://www.google.com/')
p_id = create_product(product, c_id)

product_history = ProductHistory(price=11, currency='Dollar', date_time_scrap=datetime.now() + timedelta(hours=23))
ph_id = create_product_history(product_history, p_id)

