#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getTeachingDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_teaching"
    }
    teachingDao = BaseDao.BaseDao(**CONFIG)
    return teachingDao
