# -*- coding: UTF-8 -*-
from vm4.dao.AdminDao import getAdminDao
from vm4.service import TeacherService
from vm4.context import CONSTANTS
from vm4.view import utils


def getStudentByNumAndName(stunum, name):
    adminDao = getAdminDao()
    filters = {
        "f_number": stunum,
        "f_name": name
    }
    return adminDao.select_one(None, filters)


def getAdminByTeacherId(teacherid):
    adminDao = getAdminDao()
    filter = {
        "f_teacher_id": teacherid
    }
    return adminDao.select_one(None, filter)


def getAllAdmin():
    adminDao = getAdminDao()
    adminList = adminDao.select_all(None, None)
    for admin in adminList:
        teacher = TeacherService.getTeacherById(admin["f_teacher_id"])
        admin["f_name"] = teacher["f_name"]
        admin["f_number"] = teacher["f_number"]
    return adminList


def deleteAmin(adminid):
    adminDao = getAdminDao()
    filter = {
        "f_id": adminid,
        "f_is_delete": CONSTANTS.ISDELETE_YES
    }
    return adminDao.update_by_primarikey_selective(None, filter);


def addAdmin(teacherid):
    adminDao = getAdminDao()
    nowtime = utils.getNowStr()
    admin = {
        "f_teacher_id": teacherid,
        "f_createtime": nowtime,
        "f_updatetime": nowtime
    }
    adminDao.save(None, admin)
