from src.scripts.queries import get_all_configurators
from src.db import ScrapConfigurator
from src.enums import ScrapWithEnum


for c in get_all_configurators():
    c = ScrapConfigurator(*c)
    scrap_func = ScrapWithEnum.filter_by_name(c.scrap_with).value.func
    scrap_func(c)
