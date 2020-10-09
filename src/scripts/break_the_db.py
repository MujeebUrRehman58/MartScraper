from src.db import db_cursor

product_table = 'Product'
history_table = 'ProductHistory'
company_table = 'Company'

for t in [history_table, product_table, company_table]:
    db_cursor.execute(f"DROP TABLE IF EXISTS {t}")

db_cursor.execute(
    f"CREATE TABLE {company_table} ("
    f"CompanyId INT(11) AUTO_INCREMENT PRIMARY KEY,"
    f" CompanyName VARCHAR(255) NOT NULL);"
)

db_cursor.execute(
    f"CREATE TABLE {product_table} ("
    f"ProductId INT(11) AUTO_INCREMENT PRIMARY KEY,"
    f" CompanyId INT(11) NOT NULL,"
    f" Name VARCHAR(255) NOT NULL,"
    f" Price DECIMAL(10, 2) NOT NULL,"
    f" Currency VARCHAR(255) NOT NULL,"
    f" DateTimeScrap DateTime NOT NULL,"
    f" URLImg VARCHAR(800),"
    f" ThumbURLImg VARCHAR(800),"
    f" CategoryName VARCHAR(255),"
    f" SubCategoryName VARCHAR(255),"
    f" URLProduct VARCHAR(800),"
    f" FOREIGN KEY (CompanyId) REFERENCES {company_table} (CompanyId));"
)

db_cursor.execute(
    f"CREATE TABLE {history_table} ("
    f"ProductHistoryId INT(11) AUTO_INCREMENT PRIMARY KEY,"
    f" ProductId INT(11) NOT NULL,"
    f" Price DECIMAL(10, 2) NOT NULL,"
    f" Currency VARCHAR(255) NOT NULL,"
    f" DateTimeScrap DateTime NOT NULL,"
    f" FOREIGN KEY (ProductId) REFERENCES {product_table} (ProductId));"
)


