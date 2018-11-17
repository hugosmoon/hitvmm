#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getTemplateDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_template"
    }
    templateDao = BaseDao.BaseDao(**CONFIG)
    return templateDao
