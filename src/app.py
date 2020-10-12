# scraper code goes here
from datetime import datetime, timedelta

from src.scripts.queries import create_company
from src.scripts.queries import create_product
from src.scripts.queries import create_product_history
from src.db import Company
from src.db import Product
from src.db import ProductHistory
