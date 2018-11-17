# -*- coding: UTF-8 -*-
from vm4.dao.StudentDao import getStudentDao
from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.dao.baseDao.page import Page


# 根据学生编号和姓名获取学生
def getStudentByNumAndName(name, stunum):
    studentDao = getStudentDao()
    filters = {
        "f_number": stunum,
        "f_name": name
    }
    return studentDao.select_one(None, filters)


# 根据学生编号获取学生
def getStudentByNum(stunum):
    studentDao = getStudentDao()
    filters = {
        "f_number": stunum,
    }
    return studentDao.select_one(None, filters)


# 根据学生编号和姓名获取学生列表
def getManyStudentByNameAndNumber(name, stunum, index):
    studentDao = getStudentDao()
    if (stunum is None) or (name is None):
        return None
    filters = {
        "orderby": "f_createtime"
    }
    if stunum is not None:
        filters["_like_f_number"] = stunum
    if stunum is not None:
        filters["_like_f_name"] = name
    page = Page(page_num=int(index))
    return studentDao.select_page(None, page, filters)


# 获取所有学生（创建时间倒序）
def getAllStudent(index):
    studentDao = getStudentDao()
    filter = {
        "orderby": "f_createtime"
    }
    page = Page(page_num=int(index))
    return studentDao.select_page(None, page, filter)


# 根据学生id获取学生
def getStudentById(stuid):
    studentDao = getStudentDao()
    filters = {
        "f_id": stuid,
    }
    return studentDao.select_one(None, filters)


# 添加学生
def addStudent(name, number, teachername, teachernumber):
    studentDao = getStudentDao()

    filter = {
        "f_number": number,
    }
    student = studentDao.select_one(None, filter);
    if student is not None:
        return student["f_id"];
    nowtime = utils.getNowStr()
    student = {
        "f_name": name,
        "f_number": number,
        "f_teacher_name": teachername,
        "f_teacher_number": teachernumber,
        "f_createtime": nowtime,
        "f_updatetime": nowtime
    }
    return studentDao.save(None, student)


# 根据学生id删除学生信息
def deleteStudent(studentid):
    studentDao = getStudentDao()
    filter = {
        "f_id": studentid,
        "f_is_delete": CONSTANTS.ISDELETE_YES,
    }
    return studentDao.update_by_primarikey_selective(None, filter)


# 获取所有学生总数
def getCountStudent():
    studentDao = getStudentDao()
    return studentDao.count(None, {})


# 通过编号和姓名获取所有学生总数
def getCountStudentByNameAndNumber(name, stunum):
    studentDao = getStudentDao()
    filters = {}
    if stunum is not None:
        filters["_like_f_number"] = stunum
    if stunum is not None:
        filters["_like_f_name"] = name
    return studentDao.count(None, filters)
