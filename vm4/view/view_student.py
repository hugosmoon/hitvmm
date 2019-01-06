# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from vm4.context.response import Response
from vm4.service import StudentService
from vm4.view import utils
from vm4.service import TeachingService
from vm4.service import ExperimentService
from vm4.service import ReportService
from vm4.service import TemplateService
from vm4.context import CONSTANTS
from django.http import FileResponse
import os, uuid
from django.utils.http import urlquote


# 登录页面
def v_login(request):
    return getloginResponse(request)


# 登录接口
def stulogin(request):
    stunum = utils.getParam(request, "stuid")
    stuname = utils.getParam(request, "stuname")
    student = StudentService.getStudentByNumAndName(stuname, stunum)
    if student != None:
        responseReturn = Response(None, None)
        response = HttpResponse(responseReturn.__str__())
        utils.setCookie(response, "stuid", str(student.id))
        utils.setCookie(response, "stuname", student.name)
        utils.setCookie(response, "stunum", student.number)
        return response
    else:
        responseReturn = Response("-1", "登录失败")
        return HttpResponse(responseReturn.__str__())


# 未完成实验
def v_index(request):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    stuname = utils.getCookie(request, "stuname")
    page = utils.getParam(request, "page")
    if (page is None) or page == "":
        page = 1
    else:
        page = int(page)
    count = TeachingService.getCountPageByStu(stuid, CONSTANTS.TEACHING_IS_RUNNING)
    countpage = 0
    i = 0
    if count > 0:
        if count % 10 > 0:
            i = 1
        countpage = count / 10 + i
    teachingRunList = TeachingService.getTeachingByStu(stuid, CONSTANTS.TEACHING_IS_RUNNING, page)
    experimentList = ExperimentService.getAllExperiment()
    # 获取用于菜单的实验列表
    experimentMenuList = []
    for experiment in experimentList:
        experimentTemp = experiment.copy()
        experimentName = experimentTemp["name"]
        if len(experimentName) > 8:
            experimentName = experimentName[0:10] + "..."
        experimentTemp["name"] = experimentName
        experimentMenuList.append(experimentTemp)

    teachingCount = getTeachingCount(stuid)
    return render(request, "index.html",
                  {"teachingList": teachingRunList, "countpage": countpage, "experimentMenuList": experimentMenuList,
                   "experimentList": experimentList, "teachingCount": teachingCount, "stuname": stuname})


# 完成实验
def v_completedexp(request):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    stuname = utils.getCookie(request, "stuname")
    page = utils.getParam(request, "page")
    if (page is None) or page == "":
        page = 1
    else:
        page = int(page)
    count = TeachingService.getCountPageByStu(stuid, CONSTANTS.TEACHING_IS_STOP)
    countpage = 0
    i = 0
    if count > 0:
        if count % 10 > 0:
            i = 1
        countpage = count / 10 + i
    teachingRunList = TeachingService.getTeachingByStu(stuid, CONSTANTS.TEACHING_IS_STOP, page)
    experimentList = ExperimentService.getAllExperiment()
    # 获取用于菜单的实验列表
    experimentMenuList = []
    for experiment in experimentList:
        experimentTemp = experiment.copy()
        experimentName = experimentTemp["name"]
        if len(experimentName) > 8:
            experimentName = experimentName[0:10] + "..."
        experimentTemp["name"] = experimentName
        experimentMenuList.append(experimentTemp)

    teachingCount = getTeachingCount(stuid)
    return render(request, "completedexp.html",
                  {"teachingList": teachingRunList, "countpage": countpage, "experimentMenuList": experimentMenuList,
                   "experimentList": experimentList, "teachingCount": teachingCount, "stuname": stuname})


# 全部实验
def v_allexperiment(request):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    stuname = utils.getCookie(request, "stuname")
    teachingCount = getTeachingCount(stuid)
    experimentList = ExperimentService.getAllExperiment()
    # 获取用于菜单的实验列表
    experimentMenuList = []
    for experiment in experimentList:
        experimentTemp = experiment.copy()
        experimentName = experimentTemp["name"]
        if len(experimentName) > 8:
            experimentName = experimentName[0:10] + "..."
        experimentTemp["name"] = experimentName
        experimentMenuList.append(experimentTemp)

    return render(request, "allexp.html", {"experimentList": experimentList, "experimentMenuList": experimentMenuList,
                                           "teachingCount": teachingCount, "stuname": stuname})


# 获取未完成实验和已完成实验数量
def getTeachingCount(stuid):
    runCount = TeachingService.getCountPageByStu(stuid, CONSTANTS.TEACHING_IS_RUNNING)
    stopCount = TeachingService.getCountPageByStu(stuid, CONSTANTS.TEACHING_IS_STOP)
    teachingCount = {"runCount": runCount, "stopCount": stopCount}
    return teachingCount


# 下载实验数据
def downloadData(request):
    dataurl = utils.getParam(request, "dataurl")
    if (dataurl is None) or dataurl == "":
        return HttpResponse()
    fileurl = CONSTANTS.DATAURL_PRE + dataurl
    if os.path.exists(fileurl) != True:
        return HttpResponse("未找到文件")
    file = open(fileurl, "rb")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote("实验数据" + filesuffix))

    return response


# 下载实验报告模板
def downloadTemplate(request):
    templateid = utils.getParam(request, "templateid")
    if (templateid is None) or templateid == "":
        return HttpResponse()
    template = TemplateService.getTemplateById(templateid)
    fileurl = CONSTANTS.TEMPLATEURL_PRE + template.url
    if os.path.exists(fileurl) != True:
        return HttpResponse("未找到文件")
    file = open(fileurl, "rb")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote("实验模板" + filesuffix))
    return response


# 提交报告
def submitReport(request):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    reportid = utils.getParam(request, "reportid")
    file = request.FILES.get('file', None)
    if file is None:
        return HttpResponse(
            "<script>if(confirm('上传的文件为空')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    if filesuffix != ".pdf":
        return HttpResponse(
            "<script>if(confirm('实验报告的格式必须为pdf')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = str(uuid.uuid1()) + ".pdf"
    fp = open(os.path.join(CONSTANTS.REPORTURL_PRE, filename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()
    ReportService.submintReport(reportid, filename)
    return HttpResponse(
        "<script>if(confirm('上传成功')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


# 获取登录页response
def getloginResponse(request):
    response = render(request, "login.html")
    response.delete_cookie("stuid")
    response.delete_cookie("stuname")
    response.delete_cookie("stunum")
    return response
