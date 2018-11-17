#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getStudentDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_student"
    }
    studentDao = BaseDao.BaseDao(**CONFIG)
    return studentDao
