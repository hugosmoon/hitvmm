# -*- coding: UTF-8 -*-
from vm4.service import TeacherService
from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.models import *
from django.forms.models import model_to_dict
from django.db import transaction


def getAdminByTeacherId(teacherid):
    try:
        admin = Admin.objects.filter(teacherid=teacherid, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return admin


def getAdminById(adminid):
    try:
        admin = Admin.objects.filter(id=adminid, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return admin


def getAllAdmin():
    try:
        adminList = Admin.objects.filter(isdelete=CONSTANTS.ISDELETE_NOT).all()
    except:
        return None
    else:
        adminDictList = []
        for admin in adminList:
            adminDict = {
                "id": admin.id,
                "teacherid": admin.teacherid,
                "isdelete": admin.isdelete,
                "createtime": admin.createtime,
                "updatetime": admin.updatetime
            }
            teacher = Teacher.objects.filter(id=admin.teacherid, isdelete=CONSTANTS.ISDELETE_NOT).get()
            adminDict['f_name'] = teacher.name
            adminDict['f_number'] = teacher.number
            adminDictList.append(adminDict)
        return adminDictList


def deleteAmin(adminid):
    try:
        admin1 = Admin.objects.filter(id=adminid, isdelete=CONSTANTS.ISDELETE_NOT).get()
        with transaction.atomic():
            admin = Admin.objects.filter(id=int(adminid), isdelete=CONSTANTS.ISDELETE_NOT).update(
                isdelete=CONSTANTS.ISDELETE_YES)
            teacher = Teacher.objects.filter(id=admin1.teacherid, isdelete=CONSTANTS.ISDELETE_NOT).update(
                isdelete=CONSTANTS.ISDELETE_YES)
    except:
        return None
    else:
        return admin


def addAdmin(teacherid):
    now = utils.getNow()
    admin = Admin(teacherid=teacherid, isdelete=CONSTANTS.ISDELETE_NOT, createtime=now, updatetime=now)
    admin.save()
    return admin.id
