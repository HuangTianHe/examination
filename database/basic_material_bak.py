#*-*coding:utf8*-*
from sqlalchemy import Table
from utils import loader

class EntityOrgAdmin(Table):
    def __new__(cls, *args, **kwargs):
        return super(EntityOrgAdmin, cls).__new__(cls, 'entity_org_admin',
                                                   loader.loader.sql_manager.neworiental_v3,
                                                   autoload = True)