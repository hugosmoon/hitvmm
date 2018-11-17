# -*- coding: UTF-8 -*-
from vm4.dao.TeacherDao import getTeacherDao
from vm4.context import CONSTANTS
from vm4.dao.baseDao.page import Page
from vm4.view import utils


# 根据id获取教师
def getTeacherById(teacherId):
    teacherDao = getTeacherDao()
    filters = {
        "f_id": teacherId
    }
    return teacherDao.select_one(None, filters)


# 根据教师编号获取教师
def getTeacherByNumber(number):
    teacherDao = getTeacherDao()
    filters = {
        "f_number": number,
    }
    return teacherDao.select_one(None, filters)


# 修改密码
def editPassword(teacher):
    teacherDao = getTeacherDao()
    return teacherDao.update_by_primarikey_selective(None, teacher)


# 添加教师
def addTeacher(name, number):
    teacherDao = getTeacherDao()
    nowtime = utils.getNowStr()
    teacher = {
        "f_name": name,
        "f_number": number,
        "f_password": CONSTANTS.DEFUALT_PASSWORD,
        "f_createtime":nowtime,
        "f_updatetime":nowtime
    }

    return teacherDao.save(None, teacher)


# 根据编号和密码获得教师
def getTeacherByNumAndPwd(number, passwrod):
    teacherDao = getTeacherDao()
    filter = {
        "f_number": number,
        "f_password": passwrod
    }
    return teacherDao.select_one(None, filter)


# 获取教师分页
def getTeacherByPage( name, number,index):
    teacherDao = getTeacherDao()
    filter = {}
    if name is not None:
        filter["_like_f_name"] = name
    if number is not None:
        filter["_like_f_number"] = number
    page = Page(page_num=int(index))
    return teacherDao.select_page(None, page, filter)


# 重置教师密码
def resetPassword(teacherid):
    teacherDao = getTeacherDao()
    teacher = {
        "f_id": teacherid,
        "f_password": CONSTANTS.DEFUALT_PASSWORD
    }
    teacherDao.update_by_primarikey_selective(None, teacher)
    return;

#删除教师
def deleteTeacher(teacherid):
    teacherDao = getTeacherDao()
    filter = {
        "f_id": teacherid,
        "f_is_delete": CONSTANTS.ISDELETE_YES,
    }
    teacherDao.update_by_primarikey_selective(None,filter)
    return;


#获取教师总数
def getCountTeacher():
    teacherDao = getTeacherDao()
    return teacherDao.count(None,{})