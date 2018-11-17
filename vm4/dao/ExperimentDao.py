#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getExperimentDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_experiment"
    }
    experimentDao = BaseDao.BaseDao(**CONFIG)
    return experimentDao
