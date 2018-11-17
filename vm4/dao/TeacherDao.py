#-*- coding: UTF-8 -*-
from vm4.dao.baseDao import BaseDao

def getTeacherDao():
    CONFIG = {
        "user": "root",
        "password": "1234",
        "database": "vmm",
        "table": "t_teacher"
    }
    teacherDao = BaseDao.BaseDao(**CONFIG)
    return teacherDao
