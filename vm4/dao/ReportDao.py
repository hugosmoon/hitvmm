#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getReportDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_report"
    }
    reportDao = BaseDao.BaseDao(**CONFIG)
    return reportDao
