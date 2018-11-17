#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getAdminDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_admin"
    }
    adminDao = BaseDao.BaseDao(**CONFIG)
    return adminDao
