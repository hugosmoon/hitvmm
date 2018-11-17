#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getVideoDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_video"
    }
    videoDao = BaseDao.BaseDao(**CONFIG)
    return videoDao
