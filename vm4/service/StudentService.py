# -*- coding: UTF-8 -*-
from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.models import *
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from vm4.service import FilterInfoService


# 根据学生编号和姓名获取学生
def getStudentByNumAndName(name, stunum):
    try:
        student = Student.objects.get(name=name, number=stunum, isdelete=CONSTANTS.ISDELETE_NOT)
    except:
        return None
    else:
        return student


# 根据学生编号获取学生
def getStudentByNum(stunum):
    try:
        student = Student.objects.filter(number=stunum, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return student


# 根据学生编号和姓名获取学生列表
def getManyStudentByNameAndNumber(name, stunum, index):
    studentsearch = Student.objects

    if stunum is not None:
        studentsearch = studentsearch.filter(number__contains=stunum, isdelete=CONSTANTS.ISDELETE_NOT)
    if stunum is not None:
        studentsearch = studentsearch.filter(name__contains=name, isdelete=CONSTANTS.ISDELETE_NOT)
    studentsearch.order_by('createtime')
    try:
        studentList = studentsearch.all()
    except:
        return None
    else:
        paginator = Paginator(studentList, 10)
        sutdentPageList = paginator.page(index)
        return sutdentPageList


# 获取所有学生（创建时间倒序）
def getAllStudent(index):
    try:
        studentList = Student.objects.filter(isdelete=CONSTANTS.ISDELETE_NOT).all().order_by('createtime')
    except:
        return None
    else:
        paginator = Paginator(studentList, 10)
        sutdentPageList = paginator.page(index)
        return sutdentPageList


# 根据学生id获取学生
def getStudentById(stuid):
    try:
        student = Student.objects.filter(id=stuid, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return student


# 添加学生
def addStudent(name, number, filterinfoid):
    now = utils.getNow()
    student = Student(name=name, number=number, filterinfoid=filterinfoid, createtime=now,
                      isdelete=CONSTANTS.ISDELETE_NOT, updatetime=now)
    student.save()
    return student.id


# 根据学生id删除学生信息
def deleteStudent(studentid):
    try:
        student = Student.objects.filter(id=studentid, isdelete=CONSTANTS.ISDELETE_NOT).update(
            isdelete=CONSTANTS.ISDELETE_YES)
    except:
        return None
    else:
        return student


# 获取所有学生总数
def getCountStudent():
    try:
        count = Student.objects.filter(isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count


# 通过编号和姓名获取所有学生总数
def getCountStudentByNameAndNumber(name, stunum):
    studentsearch = Student.objects

    if stunum is not None:
        studentsearch = studentsearch.filter(number__contains=stunum, isdelete=CONSTANTS.ISDELETE_NOT)
    if stunum is not None:
        studentsearch = studentsearch.filter(name__contains=name, isdelete=CONSTANTS.ISDELETE_NOT)

    try:
        count = studentsearch.count()
    except:
        return 0
    else:
        return count


# 根据班级id获取学生总数
def getCountStudentByFilterInfo(filterinfoid):
    try:
        count = Student.objects.filter(filterinfoid=filterinfoid, isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count


# 根据班级id获取学生列表
def getStudentListByFilterInfo(filterinfoid):
    try:
        studentList = Student.objects.filter(filterinfoid=filterinfoid, isdelete=CONSTANTS.ISDELETE_NOT).all()
    except:
        return None
    else:
        return studentList
