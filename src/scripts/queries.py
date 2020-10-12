from src.db import db
from src.db import db_cursor
from src.db import Company
from src.db import Product
from src.db import ProductHistory


def create_company(obj: Company):
    try:
        sql = "INSERT INTO Company (CompanyName) VALUES (%s)"
        db_cursor.execute(sql, (obj.company_name,))
        db.commit()
        return db_cursor.lastrowid
    except:
        return False


def create_product(obj: Product, company_id):
    try:
        sql = "INSERT INTO Product (CompanyId, Name, Price, Currency, DateTimeScrap, URLImg, ThumbURLImg," \
              " CategoryName, SubCategoryName, URLProduct) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db_cursor.execute(sql, (company_id, obj.name, obj.price, obj.currency, obj.date_time_scrap, obj.url_img,
                                obj.thumb_url_img, obj.category_name, obj.sub_category_name, obj.url_product))
        db.commit()
        p_id = db_cursor.lastrowid
        create_product_history(ProductHistory(price=obj.price, currency=obj.currency,
                                              date_time_scrap=obj.date_time_scrap), p_id)
        return p_id
    except Exception as ex:
        return False


def create_product_history(obj: ProductHistory, product_id):
    try:
        sql = "INSERT INTO ProductHistory (ProductId, Price, Currency, DateTimeScrap) VALUES (%s, %s, %s, %s)"
        db_cursor.execute(sql, (product_id, obj.price, obj.currency, obj.date_time_scrap))
        db.commit()
        return db_cursor.lastrowid
    except:
        return False


def find_product_by_name_and_company(name, company_id):
    sql = f"SELECT * FROM Product WHERE Name='{name}' AND CompanyId={company_id}"
    db_cursor.execute(sql)
    result = db_cursor.fetchone()
    return result[0] if result else result
