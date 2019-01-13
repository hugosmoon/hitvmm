# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from vm4.context.response import Response
from vm4.service import AdminService
from vm4.service import TeacherService
from vm4.service import FilterInfoService
from vm4.service import StudentService
from vm4.view import utils
from VMM import superadmin
from vm4.context import CONSTANTS
import xlrd
import xlwt
import os, uuid, json
from django.http import FileResponse
from django.utils.http import urlquote
from django.forms.models import model_to_dict


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
    filterInfoList = FilterInfoService.getFilterInfoList(None)
    filterInfoDictList = []
    for filterinfo in filterInfoList:
        dict = model_to_dict(filterinfo)
        del dict["isdelete"]
        del dict["createtime"]
        del dict["updatetime"]
        filterInfoDictList.append(dict)
    filterInfoListstr = json.dumps(filterInfoDictList, ensure_ascii=False)
    return render(request, "adduser.html",
                  {"issuperadmin": issuperadmin, "adminname": adminname, "filterInfoList": filterInfoList,
                   "filterInfoListstr": filterInfoListstr})


# 根据学生id删除学生
def deleteStudentByid(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    stuid = utils.getParam(request, "studentid")
    StudentService.deleteStudent(stuid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 重置密码
def resetTeacherPwd(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teacherid = utils.getParam(request, "teacherid")
    TeacherService.resetPassword(teacherid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 根据教师id删除教师
def deleteTeacherByid(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teacherid = utils.getParam(request, "teacherid")
    TeacherService.deleteTeacher(teacherid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 根据管理员id删除管理员
def deleteAdminByid(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
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
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    studentnum = utils.getParam(request, "studentnum")
    studentname = utils.getParam(request, "studentname")
    filterinfoid = utils.getParam(request, "filterinfoid")
    if (studentname == "" or studentnum == "" or filterinfoid == ""):
        responseReturn = Response("-1", "填写的信息不能为空！")
        return HttpResponse(responseReturn.__str__())
    student = StudentService.getStudentByNum(studentnum)
    if student is not None:
        responseReturn = Response("-1", "此学生已经存在！")
        return HttpResponse(responseReturn.__str__())

    StudentService.addStudent(studentname, studentnum, filterinfoid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 添加教师
def addTeacher(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
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
        responseReturn = Response(-2, "请登录")
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


# 获取列表模板
def getListTemplate(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
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
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(filename + '.xlsx'))
    return response;


def addBatchStudent(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    file = request.FILES.get('file', None)

    stulistfilename = file.name
    if file is None:
        return HttpResponse(
            "<script>if(confirm('请选择你要上传的学生名单！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    stulistfilename = file.name
    stulistfilesuffix = os.path.splitext(stulistfilename)[1]
    if stulistfilesuffix != ".xsl" and stulistfilesuffix != ".xlsx":
        return HttpResponse(
            "<script>if(confirm('学生名单必须为excel格式！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")

    stulistfilename = str(uuid.uuid1()) + stulistfilesuffix
    fp = open(os.path.join(CONSTANTS.STUDENTLISTURL_PRE + stulistfilename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()

    studentList, executestate, failtext = getStudentListByExcel(stulistfilename)
    if executestate == 1:
        return HttpResponse(
            "<script>if(confirm('" + failtext + "')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")

    for student in studentList:
        StudentService.addStudent(student["name"], student["number"], student["filterinfoid"])

    return HttpResponse(
        "<script>if(confirm('添加成功！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


def addBatchTeacher(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    file = request.FILES.get('file', None)

    teacherfilename = file.name
    if file is None:
        return HttpResponse(
            "<script>if(confirm('请选择你要上传的教师名单！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    teacherfilename = file.name
    tealistfilesuffix = os.path.splitext(teacherfilename)[1]
    if tealistfilesuffix != ".xsl" and tealistfilesuffix != ".xlsx":
        return HttpResponse(
            "<script>if(confirm('教师名单必须为excel格式！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")

    teacherfilename = str(uuid.uuid1()) + tealistfilesuffix
    fp = open(os.path.join(CONSTANTS.STUDENTLISTURL_PRE + teacherfilename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()

    teacherlist = getTeacherListByExcel(teacherfilename);

    for teacher in teacherlist:
        teacherobj = TeacherService.getTeacherByNumber(teacher["number"])
        if teacherobj is None:
            TeacherService.addTeacher(teacher["name"], teacher["number"])
        else:
            return HttpResponse(
                "<script>if(confirm('教师已存在，姓名：" + teacher["name"] + "，编号：" + teacher[
                    "number"] + "')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    return HttpResponse(
        "<script>if(confirm('添加成功！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


def addBatchAdmin(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    file = request.FILES.get('file', None)

    adminfilename = file.name
    if file is None:
        return HttpResponse(
            "<script>if(confirm('请选择你要上传的管理员名单！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    adminfilename = file.name
    adminlistfilesuffix = os.path.splitext(adminfilename)[1]
    if adminlistfilesuffix != ".xsl" and adminlistfilesuffix != ".xlsx":
        return HttpResponse(
            "<script>if(confirm('管理员名单必须为excel格式！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")

    adminfilename = str(uuid.uuid1()) + adminlistfilesuffix
    fp = open(os.path.join(CONSTANTS.STUDENTLISTURL_PRE + adminfilename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()

    adminlist = getAdminListByExcel(adminfilename)

    for admin in adminlist:
        teacher = TeacherService.getTeacherByNumber(admin["number"])
        if teacher is None:
            return HttpResponse(
                "<script>if(confirm('此教师" + admin[
                    "number"] + "不存在，请先添加教师！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
        if teacher.name != admin["name"]:
            return HttpResponse(
                "<script>if(confirm('教师姓名" + admin["name"] + "与教师编号" + admin[
                    "number"] + "不符，请确认!')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
        adminobj = AdminService.getAdminByTeacherId(teacher.id)
        if adminobj is not None:
            return HttpResponse(
                "<script>if(confirm('此教师" + admin[
                    "number"] + "已经设置过管理员!')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
        adminid = AdminService.addAdmin(teacher.id)

    return HttpResponse(
        "<script>if(confirm('添加成功！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


# 获取登录页response
def getloginResponse(request):
    response = render(request, "adminlogin.html")
    response.delete_cookie("issuperadmin")
    response.delete_cookie("adminid")
    response.delete_cookie("adminname")
    return response


# 根据学生名单获取学生列表
def getStudentListByExcel(filename):
    executestate = 0  # 执行状态 0：成功，1：失败
    failtext = ""  # 失败信息
    studentlist = []
    book = xlrd.open_workbook(CONSTANTS.STUDENTLISTURL_PRE + filename)
    sheet0 = book.sheet_by_index(0)
    nrows = sheet0.nrows  # 获取行总数
    for i in range(nrows):
        if i == 0:
            continue;
        row_data = sheet0.row_values(i)
        registyear = str(int(sheet0.cell_value(i, 2)))
        major = str(int(sheet0.cell_value(i, 3)))
        classname = str(int(sheet0.cell_value(i, 4)))
        filterinfo = FilterInfoService.getFilterInfo(registyear, major, classname)
        if filterinfo is None:
            executestate = 1
            failtext = """班级不存在，入学年份：%s，院系：%s，班级：%s""" % (registyear, major, classname)
            return studentlist, executestate, failtext

        student = {
            "name": sheet0.cell_value(i, 0),
            "number": str(int(sheet0.cell_value(i, 1))),
            "filterinfoid": filterinfo.id
        }
        studentobj = StudentService.getStudentByNum(student["number"])
        if studentobj is not None:
            executestate = 1
            failtext = """该学生已存在，姓名：%s，学号：%s""" % (student["name"], student["number"])
            return studentlist, executestate, failtext
        studentlist.append(student)
    return studentlist, executestate, failtext


# 根据老师名单获取老师列表
def getTeacherListByExcel(filename):
    teacherlist = []
    book = xlrd.open_workbook(CONSTANTS.STUDENTLISTURL_PRE + filename)
    sheet0 = book.sheet_by_index(0)
    nrows = sheet0.nrows  # 获取行总数
    for i in range(nrows):
        if i == 0:
            continue;
        row_data = sheet0.row_values(i)
        teacher = {
            "name": sheet0.cell_value(i, 0),
            "number": sheet0.cell_value(i, 1),
        }
        teacherlist.append(teacher)
    return teacherlist


# 根据管理员名单获取管理员列表
def getAdminListByExcel(filename):
    adminlist = []
    book = xlrd.open_workbook(CONSTANTS.STUDENTLISTURL_PRE + filename)
    sheet0 = book.sheet_by_index(0)
    nrows = sheet0.nrows  # 获取行总数
    for i in range(nrows):
        if i == 0:
            continue;
        row_data = sheet0.row_values(i)
        admin = {
            "name": sheet0.cell_value(i, 0),
            "number": sheet0.cell_value(i, 1),
        }
        adminlist.append(admin)
    return adminlist


# 设置学生基础信息
def setBasicInformation(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        return getloginResponse(request)
    filterInfoList = FilterInfoService.getFilterInfoList(None)
    issuperadmin = utils.getCookie(request, "issuperadmin")
    adminname = utils.getCookie(request, "adminname")
    return render(request, "set_basic_information.html",
                  {"filterInfoList": filterInfoList, "issuperadmin": issuperadmin, "adminname": adminname})


# 添加过滤信息
def addFilterInfo(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    registyear = utils.getParam(request, "registyear")
    major = utils.getParam(request, "major")
    classname = utils.getParam(request, "classname")
    if registyear is None or registyear == "":
        responseReturn = Response(-1, "请输入入学年份~")
        return HttpResponse(responseReturn.__str__())

    if major is None or major == "":
        responseReturn = Response(-1, "请输入院系~")
        return HttpResponse(responseReturn.__str__())

    if classname is None or classname == "":
        responseReturn = Response(-1, "请输入班级~")
        return HttpResponse(responseReturn.__str__())

    filterinfo = FilterInfoService.getFilterInfo(registyear, major, classname)
    if filterinfo is None:
        filterinfoid = FilterInfoService.addFilterInfo(registyear, major, classname)
        responseReturn = Response(None, None)
        return HttpResponse(responseReturn.__str__())
    else:
        responseReturn = Response(-1, "已有此班级，请重新输入~")
        return HttpResponse(responseReturn.__str__())


# 删除过滤信息
def delFilterInfo(request):
    adminid = utils.getCookie(request, "adminid")
    if adminid == "" or adminid is None:
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())

    filterid = utils.getParam(request, "filterid")
    if filterid == "" or filterid is None:
        responseReturn = Response(-1, "请选择一个班级")
        return HttpResponse(responseReturn.__str__())

    filterinfo = FilterInfoService.getFilterInfoById(filterid);
    if filterinfo is None:
        responseReturn = Response(-1, "此班级不存在~")
        return HttpResponse(responseReturn.__str__())

    count = StudentService.getCountStudentByFilterInfo(filterid)
    if count > 0:
        responseReturn = Response(-1, "该班级下还有同学，不能删除哦~")
        return HttpResponse(responseReturn.__str__())

    filterdelinfo = FilterInfoService.delFilterInfo(filterid)
    if filterdelinfo is None:
        responseReturn = Response(-1, "删除失败，请重试！")
        return HttpResponse(responseReturn.__str__())

    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())
