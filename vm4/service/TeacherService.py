# -*- coding: UTF-8 -*-
from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.models import *
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

# 根据id获取教师
def getTeacherById(teacherId):
    try:
        teacher = Teacher.objects.filter(id=teacherId, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return teacher


# 根据教师编号获取教师
def getTeacherByNumber(number):
    try:
        teacher = Teacher.objects.filter(number=number, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return teacher


# 修改密码
def editPassword(teacherid, newpwd):
    try:
        teacher = Teacher.objects.filter(id=teacherid, isdelete=CONSTANTS.ISDELETE_NOT).update(password=newpwd)
    except:
        return None
    else:
        return teacher


# 添加教师
def addTeacher(name, number):
    now = utils.getNow()
    teacher = Teacher(name=name, number=number, password=CONSTANTS.DEFUALT_PASSWORD, isdelete=CONSTANTS.ISDELETE_NOT,
                      createtime=now, updatetime=now)
    teacher.save()
    return teacher.id


# 根据编号和密码获得教师
def getTeacherByNumAndPwd(number, passwrod):
    try:
        teacher = Teacher.objects.filter(number=number, password=passwrod, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return teacher


# 获取教师分页
def getTeacherByPage(name, number, index):
    teachersearch = Teacher.objects.filter(isdelete=CONSTANTS.ISDELETE_NOT)
    if name is not None:
        teachersearch = teachersearch.filter(name__contains=name)
    if number is not None:
        teachersearch = teachersearch.filter(number__contains=number)
    try:
        teacherList = teachersearch.all()
    except:
        return None
    else:
        paginator = Paginator(teacherList, 10)
        teacherPageList = paginator.page(index)
        return teacherPageList


# 重置教师密码
def resetPassword(teacherid):
    try:
        teacher = Teacher.objects.filter(id=teacherid, isdelete=CONSTANTS.ISDELETE_NOT).update(
            password=CONSTANTS.DEFUALT_PASSWORD, updatetime=utils.getNow())
    except:
        return None
    else:
        return teacher


# 删除教师
def deleteTeacher(teacherid):
    try:
        teacher = Teacher.objects.filter(id=teacherid, isdelete=CONSTANTS.ISDELETE_NOT).update(
            isdelete=CONSTANTS.ISDELETE_YES)
    except:
        return None
    else:
        return teacher


# 获取教师总数
def getCountTeacher():
    try:
        count = Teacher.objects.filter(isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count
