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
    f" ProductNamePath VARCHAR(800) NOT NULL,"
    f" ProductPricePath VARCHAR(800) NOT NULL,"
    f" ProductThumbImgPath VARCHAR(800) NOT NULL,"
    f" ProductImgPath VARCHAR(800),"
    f" PaginationPath VARCHAR(800),"
    f" CategoryNamePath VARCHAR(800),"
    f" SubCategoryNamePath VARCHAR(800),"
    f" SubSubCategoryNamePath VARCHAR(800),"
    f" ExternalProductIdPath VARCHAR(800),"
    f" ProductItemsPath VARCHAR(800),"
    f" ProductURLPath VARCHAR(800),"
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
    f" ExternalProductId INT(11) NOT NULL,"
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


# create scrap configurator for Geant
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.GEANT.value),
    scrap_with=ScrapWithEnum.API.name,
    product_name_path="['productName']",
    product_price_path="['items', '0', 'sellers', '0', 'commertialOffer', 'Price']",
    product_thumb_img_path="['items', '0', 'images', '0', 'imageUrl']",
    product_img_path="['items', '0', 'images', '0', 'imageUrl']",
    pagination_path=None,
    category_name_path="['categories', '0']",
    sub_category_name_path="['categories', '0']",
    sub_sub_category_name_path="['categories', '0']",
    external_product_id_path="['productId']",
    product_items_path=None,
    product_url_path="['link']",
    url=None,
    api="https://www.geant.com.uy/api/catalog_system/pub/products/search/"
        "papeleria?O=OrderByReleaseDateDESC&_from={}&_to={}&ft"
))

# create scrap configurator for Devoto
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.DEVOTO.value),
    scrap_with=ScrapWithEnum.API_BS.name,
    product_name_path="['productName']",
    product_price_path="['items', '0', 'sellers', '0', 'commertialOffer', 'Price']",
    product_thumb_img_path="['items', '0', 'images', '0', 'imageUrl']",
    product_img_path="['items', '0', 'images', '0', 'imageUrl']",
    pagination_path=None,
    category_name_path="['categories', '0']",
    sub_category_name_path="['categories', '0']",
    sub_sub_category_name_path="['categories', '0']",
    external_product_id_path="['productId']",
    product_items_path='.Product',
    product_url_path="['link']",
    url="https://www.devoto.com.uy/buscapagina?sc=3&fq=C%3a%2f412%2f&"
        "PS=20&sl=994d903c-157c-4807-b8a3-ae3c5e511a30&cc=1&sm=0&PageNumber={}",
    api="https://www.devoto.com.uy/api/catalog_system/pub/products/search/?&fq=productId:{}",
))

# create scrap configurator for Tata
for c in ['desayuno', 'aceites-y-aderezos', 'golosinas-y-chocolates', 'panificados',
          'snacks', 'aceitunas-y-encurtidos', 'conservas', 'arroz-harina-y-legumbres',
          'sopas-caldos-y-pure', 'pastas-y-salsas', 'apto-para-celiacos-y-diabeticos']:
    create_scrap_configurator(ScrapConfigurator(
        company_id=get_company_by_name(CompanyNameEnum.TATA.value),
        scrap_with=ScrapWithEnum.API.name,
        product_name_path="['productName']",
        product_price_path="['items', '0', 'sellers', '0', 'commertialOffer', 'Price']",
        product_thumb_img_path="['items', '0', 'images', '0', 'imageUrl']",
        product_img_path="['items', '0', 'images', '0', 'imageUrl']",
        pagination_path=None,
        category_name_path="['categories', '0']",
        sub_category_name_path="['categories', '0']",
        sub_sub_category_name_path="['categories', '0']",
        external_product_id_path="['productId']",
        product_items_path=None,
        product_url_path="['link']",
        url=None,
        api=f"https://www.tata.com.uy/api/catalog_system/pub/products/search/almacen/{c}"
            "?O=OrderByTopSaleDESC&_from={}&_to={}&ft&sc=4"
))

# create scrap configurator for Disco
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.DISCO.value),
    scrap_with=ScrapWithEnum.API_BS.name,
    product_name_path="['productName']",
    product_price_path="['items', '0', 'sellers', '0', 'commertialOffer', 'Price']",
    product_thumb_img_path="['items', '0', 'images', '0', 'imageUrl']",
    product_img_path="['items', '0', 'images', '0', 'imageUrl']",
    pagination_path=None,
    category_name_path="['categories', '0']",
    sub_category_name_path="['categories', '0']",
    sub_sub_category_name_path="['categories', '0']",
    external_product_id_path="['productId']",
    product_items_path='.Product',
    product_url_path="['link']",
    url="https://www.disco.com.uy/buscapagina?sc=4&fq=C%3a%2f412%2f&" \
        "PS=20&sl=994d903c-157c-4807-b8a3-ae3c5e511a30&cc=1&sm=0&PageNumber={}",
    api="https://www.disco.com.uy/api/catalog_system/pub/products/search/?&fq=productId:{}"
))

# create scrap configurator for Tiendainglesa
create_scrap_configurator(ScrapConfigurator(
    company_id=get_company_by_name(CompanyNameEnum.TIENDAINGLESA.value),
    scrap_with=ScrapWithEnum.SELENIUM.name,
    product_name_path='.wCartProductName a',
    product_price_path='.ProductPrice',
    product_thumb_img_path='.gx-image-link img',
    product_img_path='.gx-image-link img',
    pagination_path=None,
    category_name_path='.wBreadCrumbText a',
    sub_category_name_path='.wBreadCrumbText a',
    sub_sub_category_name_path='.wBreadCrumbText a',
    external_product_id_path=None,
    product_items_path='.TableWebGridSearch',
    product_url_path='.wCartProductName a',
    url='https://www.tiendainglesa.com.uy/Categoria/Almac%C3%A9n/'
        'busqueda?0,0,*:*,78,0,0,,%5B%5D,false,%5B%5D,%5B%5D,,{}',
    api=None
))
