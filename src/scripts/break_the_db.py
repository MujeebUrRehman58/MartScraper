from src.db import db_cursor
from src.db import Company
from src.db import ScrapConfigurator
from src.scripts.queries import create_company
from src.scripts.queries import create_scrap_configurator
from src.scripts.queries import get_company_by_name
from src.enums import TablesEnum
from src.enums import CompanyNameEnum
from src.enums import ScrapWithEnum


for t in TablesEnum.list():
    db_cursor.execute(f"DROP TABLE IF EXISTS {t}")

db_cursor.execute(
    f"CREATE TABLE {TablesEnum.COMPANY.value} ("
    f"CompanyId INT(11) AUTO_INCREMENT PRIMARY KEY,"
    f" CompanyName VARCHAR(255) NOT NULL);"
)

db_cursor.execute(
    f"CREATE TABLE {TablesEnum.SCRAP_CONFIGURATOR.value} ("
    f"ScrapConfiguratorID INT(11) AUTO_INCREMENT PRIMARY KEY,"
    f" CompanyId INT(11) NOT NULL,"
    f" ScrapWith VARCHAR(255) NOT NULL,"
    f" ProductItemsPath VARCHAR(800) NOT NULL,"
    f" ProductNamePath VARCHAR(800) NOT NULL,"
    f" ProductPricePath VARCHAR(800) NOT NULL,"
    f" ProductThumbImgPath VARCHAR(800) NOT NULL,"
    f" ProductImgPath VARCHAR(800),"
    f" PaginationPath VARCHAR(800),"
    f" CategoryNamePath VARCHAR(800),"
    f" SubCategoryNamePath VARCHAR(800),"
    f" SubSubCategoryNamePath VARCHAR(800),"
    f" URL VARCHAR(800),"
    f" API VARCHAR(800),"
    f" FOREIGN KEY (CompanyId) REFERENCES {TablesEnum.COMPANY.value} (CompanyId));"
)

db_cursor.execute(
    f"CREATE TABLE {TablesEnum.PRODUCT.value} ("
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
    f" SubSubCategoryName VARCHAR(255),"
    f" URLProduct VARCHAR(800),"
    f" FOREIGN KEY (CompanyId) REFERENCES {TablesEnum.COMPANY.value} (CompanyId));"
)

db_cursor.execute(
    f"CREATE TABLE {TablesEnum.HISTORY.value} ("
    f"ProductHistoryId INT(11) AUTO_INCREMENT PRIMARY KEY,"
    f" ProductId INT(11) NOT NULL,"
    f" Price DECIMAL(10, 2) NOT NULL,"
    f" Currency VARCHAR(255) NOT NULL,"
    f" DateTimeScrap DateTime NOT NULL,"
    f" FOREIGN KEY (ProductId) REFERENCES {TablesEnum.PRODUCT.value} (ProductId));"
)

# create companies
for e in CompanyNameEnum.list():
    create_company(Company(e))

# create scrap configurator for Tiendainglesa
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.TIENDAINGLESA.value),
    scrap_with=ScrapWithEnum.SELENIUM.name,
    product_items_path='.TableWebGridSearch',
    product_name_path='.wCartProductName a',
    product_price_path='.ProductPrice',
    product_thumb_img_path='.gx-image-link img',
    product_img_path='.gx-image-link img',
    pagination_path=None,
    category_name_path='.wBreadCrumbText a',
    sub_category_name_path='.wBreadCrumbText a',
    sub_sub_category_name_path='.wBreadCrumbText a',
    url='https://www.tiendainglesa.com.uy/Categoria/Almac%C3%A9n/'
        'busqueda?0,0,*:*,78,0,0,,%5B%5D,false,%5B%5D,%5B%5D,,{}',
    api=None
))

'''
# create scrap configurator for Tata
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.TIENDAINGLESA.value), 
    scrap_with=ScrapWithEnum.SELENIUM.name,
    product_name_path='.wCartProductName a',
    product_price_path='',
    product_thumb_img_path='',
    product_img_path='',
    pagination_path='',
    category_name_path='',
    sub_category_name_path='',
    sub_sub_category_name_path='',
    url='',
    api=''
))

# create scrap configurator for Disco
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.TIENDAINGLESA.value), 
    scrap_with=ScrapWithEnum.SELENIUM.name,
    product_name_path='.wCartProductName a',
    product_price_path='',
    product_thumb_img_path='',
    product_img_path='',
    pagination_path='',
    category_name_path='',
    sub_category_name_path='',
    sub_sub_category_name_path='',
    url='',
    api=''
))
'''