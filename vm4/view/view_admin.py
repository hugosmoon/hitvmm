# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from vm4.context.response import Response
from vm4.service import AdminService
from vm4.service import TeacherService
from vm4.service import StudentService
from vm4.view import utils
from VMM import superadmin
from vm4.context import CONSTANTS
import os
from django.http import FileResponse


# 管理员登录页
def v_login(request):
    return render(request, "adminlogin.html")


# 管理员登录
def adminlogin(request):
    superuser = superadmin.user
    superpwd = superadmin.password

    adminid = utils.getParam(request, "adminid")
    adminpwd = utils.getParam(request, "adminpwd")

    if superuser == adminid and superpwd == adminpwd:
        responseReturn = Response(None, None)
        response = HttpResponse(responseReturn.__str__())
        utils.setCookie(response, "issuperadmin", "1")
        utils.setCookie(response, "adminid", "0")
        utils.setCookie(response, "adminname", str("superadmin"))
        return response
    teacher = TeacherService.getTeacherByNumAndPwd(adminid, adminpwd)
    if teacher is None:
        responseReturn = Response("-1", "用户名或密码错误")
        return HttpResponse(responseReturn.__str__())
    admin = AdminService.getAdminByTeacherId(teacher.id)
    if admin is not None:
        responseReturn = Response(None, None)
        response = HttpResponse(responseReturn.__str__())
        utils.setCookie(response, "issuperadmin", "0")
        utils.setCookie(response, "adminid", admin.id)
        utils.setCookie(response, "adminname", teacher.name)
        return response
    else:
        responseReturn = Response("-1", "登录失败")
        return HttpResponse(responseReturn.__str__())


# 学生管理页
def v_studentmanagement(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    issuperadmin = utils.getCookie(request, "issuperadmin")
    adminname = utils.getCookie(request, "adminname")
    stunum = utils.getParam(request, "searchnum")
    name = utils.getParam(request, "searchname")
    page = utils.getParam(request, "page")
    if (page is None) or page == "":
        page = 1
    else:
        page = int(page)

    if (stunum == "" or stunum is None) and (name == "" or name is None):
        count = StudentService.getCountStudent()
        countpage = 0
        i = 0
        if count > 0:
            if count % 10 > 0:
                i = 1
            countpage = count / 10 + i
        studentList = StudentService.getAllStudent(page)
    else:
        count = StudentService.getCountStudentByNameAndNumber(name, stunum)
        countpage = 0
        i = 0
        if count > 0:
            if count % 10 > 0:
                i = 1
            countpage = count / 10 + i
        studentList = StudentService.getManyStudentByNameAndNumber(name, stunum, page)
    param = "?"
    if stunum != "":
        param = param + "searchnum=" + stunum
    if name != "":
        if param != "?":
            param = param + "&"
        param = param + "searchname=" + name
    if param == "?":
        param = ""
    return render(request, "studentmanagement.html",
                  {"studentList": studentList, "stunum": stunum, "searchname": name, "adminname": adminname,
                   "countpage": countpage, "issuperadmin": issuperadmin})


# 管理员管理页
def v_adminmanagement(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    issuperadmin = utils.getCookie(request, "issuperadmin")
    if issuperadmin != "1" or issuperadmin is None:
        return getloginResponse(request)
    adminList = AdminService.getAllAdmin();
    return render(request, "adminmanagement.html", {"issuperadmin": issuperadmin, "adminList": adminList})


# 教师管理页
def v_teachermanagement(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    issuperadmin = utils.getCookie(request, "issuperadmin")
    teachernum = utils.getParam(request, "searchnum")
    teachername = utils.getParam(request, "searchname")
    adminname = utils.getCookie(request, "adminname")
    page = utils.getParam(request, "page")
    if (page is None) or page == "":
        page = 1
    else:
        page = int(page)
    if (teachernum == "" or teachernum is None) and (teachername == "" or teachername is None):
        count = TeacherService.getCountTeacher()
        countpage = 0
        i = 0
        if count > 0:
            if count % 10 > 0:
                i = 1
            countpage = count / 10 + i
        teacherList = TeacherService.getTeacherByPage(None, None, page)
    else:
        count = TeacherService.getCountTeacher()
        countpage = 0
        i = 0
        if count > 0:
            if count % 10 > 0:
                i = 1
            countpage = count / 10 + i
        teacherList = TeacherService.getTeacherByPage(teachername, teachernum, page)

    return render(request, "teachermanagement.html",
                  {"teacherList": teacherList, "issuperadmin": issuperadmin, "stunum": teachernum,
                   "countpage": countpage, "searchname": teachername, "adminname": adminname})


def v_adduser(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    issuperadmin = utils.getCookie(request, "issuperadmin")
    adminname = utils.getCookie(request, "adminname")

    return render(request, "adduser.html", {"issuperadmin": issuperadmin, "adminname": adminname})


# 根据学生id删除学生
def deleteStudentByid(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    stuid = utils.getParam(request, "studentid")
    StudentService.deleteStudent(stuid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 重置密码
def resetTeacherPwd(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response("-1", "请登录")
        return HttpResponse(responseReturn.__str__())
    teacherid = utils.getParam(request, "teacherid")
    TeacherService.resetPassword(teacherid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 根据教师id删除教师
def deleteTeacherByid(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    teacherid = utils.getParam(request, "teacherid")
    TeacherService.deleteTeacher(teacherid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 根据管理员id删除管理员
def deleteAdminByid(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response("-1", "请登录！")
        return HttpResponse(responseReturn.__str__())
    issuperadmin = utils.getCookie(request, "issuperadmin")
    if issuperadmin != "1" or issuperadmin is None:
        responseReturn = Response("-1", "您不是超级管理员，没有删除管理员的权限！")
        return HttpResponse(responseReturn.__str__())
    deleteadminid = utils.getParam(request, "adminid")
    admin = AdminService.deleteAmin(deleteadminid)
    if admin is None:
        responseReturn = Response("-1", "删除失败！")
        return HttpResponse(responseReturn.__str__())
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 添加学生
def addStudent(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response("-1", "请登录！")
        return HttpResponse(responseReturn.__str__())
    studentnum = utils.getParam(request, "studentnum")
    studentname = utils.getParam(request, "studentname")
    teachername = utils.getParam(request, "addteachername")
    teachernumber = utils.getParam(request, "addteachernumber")
    if (studentname == "" or studentnum == "" or teachername == "" or teachernumber == ""):
        responseReturn = Response("-1", "填写的信息不能为空！")
        return HttpResponse(responseReturn.__str__())
    # teacher = TeacherService.getTeacherByNumber(teachernumber)
    # if teacher is None :
    #    responseReturn = Response("-1", "填写的指导老师不存在！")
    #    return HttpResponse(responseReturn.__str__())
    # if teacher["f_name"] != teachername:
    #    responseReturn = Response("-1", "指导老师姓名有误！")
    #    return HttpResponse(responseReturn.__str__())
    student = StudentService.getStudentByNum(studentnum)
    if student is not None:
        responseReturn = Response("-1", "此学生已经存在！")
        return HttpResponse(responseReturn.__str__())

    StudentService.addStudent(studentname, studentnum, teachername, teachernumber)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 添加教师
def addTeacher(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response("-1", "请登录！")
        return HttpResponse(responseReturn.__str__())
    teachernum = utils.getParam(request, "teachernum")
    teachername = utils.getParam(request, "teachername")
    if (teachername == "" or teachernum == ""):
        responseReturn = Response("-1", "填写的信息不能为空！")
        return HttpResponse(responseReturn.__str__())
    teacher = TeacherService.getTeacherByNumber(teachernum)
    if teacher is not None:
        responseReturn = Response("-1", "此教师已经存在！")
        return HttpResponse(responseReturn.__str__())
    TeacherService.addTeacher(teachername, teachernum)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 添加管理员
def addAdmin(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response("-1", "请登录！")
        return HttpResponse(responseReturn.__str__())
    teachernum = utils.getParam(request, "teachernum")
    teachername = utils.getParam(request, "teachername")
    if (teachername == "" or teachernum == ""):
        responseReturn = Response("-1", "填写的信息不能为空！")
        return HttpResponse(responseReturn.__str__())
    teacher = TeacherService.getTeacherByNumber(teachernum)
    if teacher is None:
        responseReturn = Response("-1", "此教师不存在，请先添加教师！")
        return HttpResponse(responseReturn.__str__())
    if teacher.name != teachername:
        responseReturn = Response("-1", "教师姓名与教师编号不符，请确认！")
        return HttpResponse(responseReturn.__str__())
    admin = AdminService.getAdminByTeacherId(teacher.id)
    if admin is not None:
        responseReturn = Response("-1", "此教师已经设置过管理员！")
        return HttpResponse(responseReturn.__str__())
    adminid = AdminService.addAdmin(teacher.id)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


def getListTemplate(request):
    type = utils.getParam(request, "type")
    if type is None or type == "":
        responseReturn = Response("-1", "！")
        return HttpResponse(responseReturn.__str__())
    templateaddr = ""
    filename = ""
    if type == CONSTANTS.ADD_USER_TYPE_STUDENT:
        templateaddr = CONSTANTS.ADDUSERTEMPLATEURL_PRE + "student.xlsx"
        filename = "学生名单模板"
    elif type == CONSTANTS.ADD_USER_TYPE_TEACHER:
        templateaddr = CONSTANTS.ADDUSERTEMPLATEURL_PRE + "teacher.xlsx"
        filename = "教师名单模板"
    elif type == CONSTANTS.ADD_USER_TYPE_ADMIN:
        templateaddr = CONSTANTS.ADDUSERTEMPLATEURL_PRE + "admin.xlsx"
        filename = "管理员名单模板"
    if os.path.exists(templateaddr) != True:
        return HttpResponse("未找到文件")
    file = open(templateaddr, "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment';
    response['filename'] = filename + '.xlsx'
    return response;


# 获取登录页response
def getloginResponse(request):
    response = render(request, "adminlogin.html")
    response.delete_cookie("issuperadmin")
    response.delete_cookie("adminid")
    response.delete_cookie("adminname")
    return response
