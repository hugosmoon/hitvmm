# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from vm4.context.response import Response
from vm4.view import utils
from vm4.service import TeachingService
from vm4.service import TeacherService
from vm4.service import ExperimentService
from vm4.service import ReportService
from vm4.service import StudentService
from vm4.service import TemplateService
from vm4.service import FilterInfoService
from vm4.service import VideoService
from vm4.context import CONSTANTS
from django.http import FileResponse
import xlrd
import xlwt
import datetime
import os, uuid, json
from django.utils.http import urlquote
from django.forms.models import model_to_dict


# 教师登录
def v_login(request):
    return render(request, "teacherlogin.html")


# 登录接口
def teacherlogin(request):
    number = utils.getParam(request, "teaid")
    passwd = utils.getParam(request, "passwd")
    teacher = TeacherService.getTeacherByNumber(number)
    if (teacher is None) or (teacher.password != passwd):
        responseReturn = Response("-1", "登录失败")
        return HttpResponse(responseReturn.__str__())
    else:
        responseReturn = Response(None, None)
        response = HttpResponse(responseReturn.__str__())
        utils.setCookie(response, "teacherid", str(teacher.id))
        utils.setCookie(response, "teachernumber", teacher.number)
        utils.setCookie(response, "teachername", teacher.name)
        return response


# 修改密码页面
def v_password(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        return getloginResponse(request)
    teachername = utils.getCookie(request, "teachername")
    return render(request, "password.html", {"teachername": teachername})


# 修改密码
def editpassword(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    newpwd = utils.getParam(request, "newpwd")
    oldpwd = utils.getParam(request, "oldpwd")
    teacher = TeacherService.getTeacherById(teacherid)
    if oldpwd != teacher.password:
        responseReturn = Response("-1", "原密码输入有误")
        return HttpResponse(responseReturn)
    teacher.password = newpwd
    teacher.updatetime = utils.getNow()
    result = TeacherService.editPassword(teacherid, newpwd)
    if result is not None:
        responseReturn = Response(None, None)
    else:
        responseReturn = Response("-1", "网络忙，请稍后重试！")
    response = HttpResponse(responseReturn.__str__())
    return response


# 未完成教学
def v_undoneteaching(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        return getloginResponse(request)
    teachername = utils.getCookie(request, "teachername")
    page = utils.getParam(request, "page")
    if (page is None) or page == "":
        page = 1
    else:
        page = int(page)
    count = TeachingService.getCountPageByTea(teacherid, CONSTANTS.TEACHING_IS_RUNNING)
    countpage = 0
    i = 0
    if count > 0:
        if count % 10 > 0:
            i = 1
        countpage = count / 10 + i
    teachingList = TeachingService.getTeachingByTea(teacherid, CONSTANTS.TEACHING_IS_RUNNING, page)
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

    teachingCount = getTeachingCount(teacherid)
    return render(request, "undoneteaching.html",
                  {"teachingList": teachingList, "countpage": countpage, "experimentList": experimentList,
                   "experimentMenuList": experimentMenuList, "teachingCount": teachingCount,
                   "teachername": teachername})


# 完成教学
def v_completedteaching(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        return getloginResponse(request)
    teachername = utils.getCookie(request, "teachername")
    page = utils.getParam(request, "page")
    if (page is None) or page == "":
        page = 1
    else:
        page = int(page)
    count = TeachingService.getCountPageByTea(teacherid, CONSTANTS.TEACHING_IS_STOP)
    countpage = 0
    i = 0
    if count > 0:
        if count % 10 > 0:
            i = 1
        countpage = count / 10 + i
    teachingList = TeachingService.getTeachingByTea(teacherid, CONSTANTS.TEACHING_IS_STOP, page)
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

    teachingCount = getTeachingCount(teacherid)

    return render(request, "completedteaching.html",
                  {"teachingList": teachingList, "experimentList": experimentList, "countpage": countpage,
                   "teachingCount": teachingCount, "experimentMenuList": experimentMenuList,
                   "teachername": teachername})


# 批阅报告页面
def v_approval(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        return getloginResponse(request)
    teachingid = utils.getParam(request, "teachingid")
    teachername = utils.getCookie(request, "teachername")
    reportList = ReportService.getReportByTeachingid(int(teachingid))
    return render(request, "approval.html",
                  {"reportList": reportList, "teachername": teachername})


# 批阅报告
def scoreReport(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    reportid = utils.getParam(request, "reportid")
    scorestr = utils.getParam(request, "score")
    if scorestr == "" or scorestr == "0":
        responseReturn = Response(-1, "打分异常")
        response = HttpResponse(responseReturn.__str__())
        return response
    score = int(scorestr)
    ReportService.scoreReport(reportid, score)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 查看全部实验
def v_allexperiment(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        return getloginResponse(request)
    teachername = utils.getCookie(request, "teachername")
    teachingCount = getTeachingCount(teacherid)
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

    return render(request, "allexptea.html",
                  {"experimentList": experimentList, "experimentMenuList": experimentMenuList,
                   "teachingCount": teachingCount, "teachername": teachername})


# 添加教学
def v_addexp(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        return getloginResponse(request)
    teachername = utils.getCookie(request, "teachername")
    teachingCount = getTeachingCount(teacherid)
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
    filterInfoList = FilterInfoService.getFilterInfoList(None)
    filterInfoDictList = []
    for filterinfo in filterInfoList:
        dict = model_to_dict(filterinfo)
        del dict["isdelete"]
        del dict["createtime"]
        del dict["updatetime"]
        filterInfoDictList.append(dict)
    filterInfoListstr = json.dumps(filterInfoDictList, ensure_ascii=False)

    response = render(request, "addexp.html",
                      {"teachingCount": teachingCount, "experimentList": experimentList,
                       "experimentMenuList": experimentMenuList, "teachername": teachername,
                       "filterInfoListstr": filterInfoListstr})

    return response


# 获取未完成实验和已完成实验数量
def getTeachingCount(teacherid):
    runCount = TeachingService.getCountPageByTea(teacherid, CONSTANTS.TEACHING_IS_RUNNING)
    stopCount = TeachingService.getCountPageByTea(teacherid, CONSTANTS.TEACHING_IS_STOP)
    teachingCount = {"runCount": runCount, "stopCount": stopCount}
    return teachingCount


# 获取登录页response
def getloginResponse(request):
    response = render(request, "teacherlogin.html")
    response.delete_cookie("teacherid")
    response.delete_cookie("teachernumber")
    response.delete_cookie("teachername")
    return response


# 上传视频
def uploadVideo(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    experimentid = utils.getParam(request, "experimentid")
    file = request.FILES.get('file', None)
    name = utils.getParam(request, "name")
    if experimentid == "":
        responseReturn = Response(-1, "请选择实验！")
        return HttpResponse(responseReturn.__str__())
    if file is None:
        responseReturn = Response(-1, "上传文件为空！")
        return HttpResponse(responseReturn.__str__())
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    if filesuffix != ".mp4" and filesuffix != ".rmvb":
        responseReturn = Response(-1, "视屏格式应为MP4、rmvb！")
        return HttpResponse(responseReturn.__str__())
    filename = str(uuid.uuid1()) + filesuffix
    fp = open(os.path.join(CONSTANTS.EXPERIMENTVIDEOURL_PRE, filename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()
    videoid = VideoService.saveVideo(name, filename, experimentid)
    if videoid is None:
        responseReturn = Response(-1, "上传失败，请重试！")
        return HttpResponse(responseReturn.__str__())
    video = {
        "id": videoid,
        "name": name,
        "url": filename
    }
    responseReturn = Response(None, None)
    responseReturn.setRes(json.dumps(video))
    return HttpResponse(responseReturn.__str__())


# 更新实验数据
def uploadData(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teachingid = utils.getParam(request, "teachingid")
    file = request.FILES.get('file', None)
    if file is None:
        return HttpResponse(
            "<script>if(confirm('上传的文件为空')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    if filesuffix != ".xsl" and filesuffix != ".xlsx":
        return HttpResponse(
            "<script>if(confirm('实验数据必须为excel')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = str(uuid.uuid1()) + filesuffix
    fp = open(os.path.join(CONSTANTS.DATAURL_PRE, filename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()
    TeachingService.uploadData(teachingid, filename)
    return HttpResponse(
        "<script>if(confirm('上传成功')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


# 更新实验教学模板
def updateTeachingTemplate(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teachingid = utils.getParam(request, "teachingid")
    experimentid = utils.getParam(request, "experimentid")
    file = request.FILES.get('file', None)
    if file is None:
        return HttpResponse(
            "<script>if(confirm('上传的文件为空')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    if filesuffix != ".doc" and filesuffix != ".docx":
        return HttpResponse(
            "<script>if(confirm('模板必须为word格式')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = str(uuid.uuid1()) + filesuffix
    fp = open(os.path.join(CONSTANTS.TEMPLATEURL_PRE, filename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()
    templateid = TemplateService.addTemplate(experimentid, filename)
    TeachingService.uploadTemplate(teachingid, templateid)
    return HttpResponse(
        "<script>if(confirm('上传成功')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


# 删除实验教学
def deleteTeachingByid(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teachingid = utils.getParam(request, "teachingid")
    TeachingService.deleteTeachingByid(teachingid)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 更新实验教学视频
def updateTeachingVideo(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teachingid = utils.getParam(request, "teachingid")
    videos = utils.getParam(request, "videos")
    if teachingid == "" or teachingid is None:
        responseReturn = Response(-1, "操作有误，请重试")
        return HttpResponse(responseReturn.__str__())
    if videos == "" or videos is None:
        responseReturn = Response(-1, "更换的视频不能为空")
        return HttpResponse(responseReturn.__str__())
    TeachingService.updateTeachingVideoById(teachingid, videos)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 下载实验教学的学生列表
def downloadStudentList(request):
    stulisturl = utils.getParam(request, "stulisturl")
    if (stulisturl is None) or stulisturl == "":
        return HttpResponse("请重试")
    fileurl = CONSTANTS.STUDENTLISTURL_PRE + stulisturl
    if os.path.exists(fileurl) != True:
        return HttpResponse("未找到文件")
    file = open(fileurl, "rb")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote("学生名单" + filesuffix))
    return response


# 下载实验教学的学生成绩
def downloadReportScoreList(request):
    teachingid = utils.getParam(request, "teachingid")
    if teachingid == "":
        return HttpResponse(
            "<script>if(confirm('请重试！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    reportlist = ReportService.getReportByTeachingid(int(teachingid))
    if reportlist is None:
        return HttpResponse(
            "<script>if(confirm('请重试！')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = "reportsocre_" + teachingid + ".xls"
    fileurl = CONSTANTS.REPORTSCOREURL_PRE + filename
    if os.path.exists(fileurl) == True:
        os.remove(fileurl)
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('学生成绩', cell_overwrite_ok=True)
    title1 = '姓名'
    title2 = '学号'
    title3 = '报告状态'
    title4 = '成绩'
    sheet.write(0, 0, title1.decode('utf-8'))
    sheet.write(0, 1, title2.decode('utf-8'))
    sheet.write(0, 2, title3.decode('utf-8'))
    sheet.write(0, 3, title4.decode('utf-8'))
    index = 0
    for report in reportlist:
        index += 1
        sheet.write(index, 0, report["stuname"])
        sheet.write(index, 1, report["stunumber"])
        if report["f_status"] == 0:
            txt1 = "未提交报告"
            sheet.write(index, 2, txt1.decode('utf-8'))
        elif report["f_status"] == 1:
            txt1 = "未批阅"
            sheet.write(index, 2, txt1.decode('utf-8'))
        else:
            txt1 = "批阅完成"
            sheet.write(index, 2, txt1.decode('utf-8'))
        sheet.write(index, 3, report["f_score"])
    book.save(fileurl)
    file = open(fileurl, "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote("学生成绩.xls"))
    return response


# 更新实验教学截止时间
def updateTeachingDeadline(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teachingid = utils.getParam(request, "teachingid")
    deadlinestr = utils.getParam(request, "deadline") + " 00:00:00"
    deadline = datetime.datetime.strptime(deadlinestr, "%Y-%m-%d %H:%M:%S")
    TeachingService.updateTeachingDeadlineById(teachingid, deadline)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 更新实验教学教师提示
def updateTeachingPoint(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    teachingid = utils.getParam(request, "teachingid")
    point = utils.getParam(request, "point")
    TeachingService.updateTeachingPointById(teachingid, point)
    responseReturn = Response(None, None)
    return HttpResponse(responseReturn.__str__())


# 下载报告
def downloadReport(request):
    reproturl = utils.getParam(request, "reproturl")
    if (reproturl is None) or reproturl == "":
        return HttpResponse("请重试")
    fileurl = CONSTANTS.REPORTURL_PRE + reproturl
    if os.path.exists(fileurl) != True:
        return HttpResponse("未找到文件")
    file = open(fileurl, "rb")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote("实验报告" + filesuffix))
    return response


# 添加实验
def addexperiment(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    experimentid = utils.getParam(request, "experimentid")
    deadlinestr = utils.getParam(request, "deadline") + " 00:00:00"
    templatetype = utils.getParam(request, "templatetype")
    videotype = utils.getParam(request, "videotype")
    datatype = utils.getParam(request, "datatype")
    videoids = utils.getParam(request, "videos")
    point = utils.getParam(request, "point")
    remark = utils.getParam(request, "remark")
    studentids = utils.getParam(request, "studentids")
    '''
        获得实验详情
    '''
    experiment = ExperimentService.getExperimentById(experimentid)
    if experiment is None:
        responseReturn = Response(-1, "选择实验异常！")
        return HttpResponse(responseReturn.__str__())
    try:
        deadline = datetime.datetime.strptime(deadlinestr, "%Y-%m-%d %H:%M:%S")
    except:
        responseReturn = Response(-1, "请选择报告提交截止日期！")
        return HttpResponse(responseReturn.__str__())
    '''
        获得模板
    '''
    if templatetype == "1":
        templateid = experiment.templateid
    else:  # 文件上传
        templatefile = request.FILES.get('templatefile', None)
        if templatefile is None:
            responseReturn = Response(-1, "请选择你要上传的模板文件！")
            return HttpResponse(responseReturn.__str__())
        filename = templatefile.name
        filesuffix = os.path.splitext(filename)[1]
        if filesuffix != ".doc" and filesuffix != ".docx":
            responseReturn = Response(-1, "模板必须为word格式！")
            return HttpResponse(responseReturn.__str__())
        filename = str(uuid.uuid1()) + filesuffix
        fp = open(os.path.join(CONSTANTS.DATAURL_PRE, filename), 'wb+')
        for chunk in templatefile.chunks():  # 分块写入文件
            fp.write(chunk)
        fp.close()
        templateid = TemplateService.addTemplate(experimentid, filename)
    '''
        获得视频
    '''
    if videotype == "1":
        videos = experiment.videos
    else:
        videos = videoids

    '''
        获得实验数据
    '''
    if datatype == "1":  # 稍后上传
        dataurl = "none"
    else:  # 上传实验数据
        datafile = request.FILES.get('datafile', None)
        if datafile is None:
            responseReturn = Response(-1, "请选择你要上传的实验数据！")
            return HttpResponse(responseReturn.__str__())
        filename = datafile.name
        filesuffix = os.path.splitext(filename)[1]
        if filesuffix != ".xsl" and filesuffix != ".xlsx":
            responseReturn = Response(-1, "实验数据必须为excel！")
            return HttpResponse(responseReturn.__str__())
        filename = str(uuid.uuid1()) + filesuffix
        fp = open(os.path.join(CONSTANTS.DATAURL_PRE, filename), 'wb+')
        for chunk in datafile.chunks():  # 分块写入文件
            fp.write(chunk)
        fp.close()
        dataurl = filename
    '''
        获得学生名单
    '''
    studentidList = studentids.split(",")
    # 添加
    teachingid = TeachingService.addTeaching(int(experimentid), deadline, teacherid, point, remark, dataurl,
                                             "", templateid, videos)
    if teachingid is None:
        responseReturn = Response(-1, "添加失败，请重试")
        return HttpResponse(responseReturn.__str__())
    for id in studentidList:
        studentobj = None
        studentobj = StudentService.getStudentById(id)
        if studentobj is None:
            TeachingService.deleteTeachingByid(teachingid)
            responseReturn = Response(-1, "选择学生异常，请重试！")
            return HttpResponse(responseReturn.__str__())
        ReportService.addReport(teachingid, studentobj.id)

    responseReturn = Response(0, "添加成功！")
    return HttpResponse(responseReturn.__str__())


# 根据学生名单获取学生列表
def getStudentListByExcel(filename):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    studentlist = []
    book = xlrd.open_workbook(CONSTANTS.STUDENTLISTURL_PRE + filename)
    sheet0 = book.sheet_by_index(0)
    nrows = sheet0.nrows  # 获取行总数
    for i in range(nrows):
        if i == 0:
            continue;
        row_data = sheet0.row_values(i)
        student = {
            "name": sheet0.cell_value(i, 0),
            "number": str(int(sheet0.cell_value(i, 1))),
        }
        studentlist.append(student)
    return studentlist


# 获取实验教学的视频
def getVideoById(request):
    videourl = utils.getParam(request, "videourl")
    if (videourl is None) or videourl == "":
        return HttpResponse("请重试")
    fileurl = CONSTANTS.EXPERIMENTVIDEOURL_PRE + videourl
    if os.path.exists(fileurl) != True:
        return HttpResponse("未找到文件")
    file = open(fileurl, "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + videourl + '"'
    return response


# 修改实验默认预习视频
def updateExperimentVideo(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    experimentid = utils.getParam(request, "experimentid")
    videos = utils.getParam(request, "videos")
    if (experimentid is None) or experimentid == "":
        responseReturn = Response(-1, "请重新选择实验！")
        return HttpResponse(responseReturn.__str__())
    if (videos is None) or videos == "":
        responseReturn = Response(-1, "修改视频异常！")
        return HttpResponse(responseReturn.__str__())
    experiment = ExperimentService.updateExperimentVideos(experimentid, videos);
    if experiment is None:
        responseReturn = Response(-1, "网络异常，请重试！")
        return HttpResponse(responseReturn.__str__())

    responseReturn = Response(0, "修改成功！")
    return HttpResponse(responseReturn.__str__())


# 修改实验默认模板
def updateExperimentTemplate(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    experimentid = utils.getParam(request, "experimentid")
    file = request.FILES.get('file', None)
    if file is None:
        return HttpResponse(
            "<script>if(confirm('上传的文件为空')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = file.name
    filesuffix = os.path.splitext(filename)[1]
    if filesuffix != ".doc" and filesuffix != ".docx":
        return HttpResponse(
            "<script>if(confirm('模板必须为word格式')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")
    filename = str(uuid.uuid1()) + filesuffix
    fp = open(os.path.join(CONSTANTS.TEMPLATEURL_PRE, filename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        fp.write(chunk)
    fp.close()
    templateid = TemplateService.addTemplate(experimentid, filename)
    ExperimentService.updateExperimentTamplate(experimentid, templateid)
    return HttpResponse(
        "<script>if(confirm('上传成功')){history.go(-1);location.reload()}else{history.go(-1);location.reload()}</script>")


# 修改实验描述
def setdescription(request):
    # 接收基础参数
    if request.method == 'POST':
        des_content = request.POST.get('des_content')
        des_id = float(request.POST.get('des_id'))
        status = ExperimentService.updateExperimentdescription(des_id, des_content);
        if status is True:
            return HttpResponse(True)
    else:
        return HttpResponse(False)


# 根据班级获取学生
def getStudentByFilterInfoId(request):
    teacherid = utils.getCookie(request, "teacherid")
    if (teacherid is None) or teacherid == "":
        responseReturn = Response(-2, "请登录")
        return HttpResponse(responseReturn.__str__())
    filterid = utils.getParam(request, "filterid")
    if (filterid == "" or filterid is None):
        responseReturn = Response(-1, "请选择班级！")
        return HttpResponse(responseReturn.__str__())
    filterinfo = FilterInfoService.getFilterInfoById(filterid)
    if filterinfo is None:
        responseReturn = Response(-1, "班级不存在！")
        return HttpResponse(responseReturn.__str__())
    studentList = StudentService.getStudentListByFilterInfo(filterid)
    if studentList is None:
        responseReturn = Response(-1, "此班级没有学生！")
        return HttpResponse(responseReturn.__str__())
    studentDictList = []
    for student in studentList:
        dict = model_to_dict(student)
        del dict["isdelete"]
        del dict["createtime"]
        del dict["updatetime"]
        dict["registyear"] = filterinfo.registyear
        dict["major"] = filterinfo.major
        dict["classname"] = filterinfo.classname
        studentDictList.append(dict)
    studentDictListStr = json.dumps(studentDictList, ensure_ascii=False)
    responseReturn = Response(None, None)
    responseReturn.setRes(studentDictListStr)
    return HttpResponse(responseReturn.__str__())
