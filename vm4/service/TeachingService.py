# -*- coding: UTF-8 -*-
from vm4.service import ReportService
from vm4.service import ExperimentService
from vm4.service import VideoService
from vm4.service import TeacherService
from vm4.view import utils
from vm4.context import CONSTANTS
import json
from vm4.models import *
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


# 根据学生id获得教学
def getTeachingByStu(stuid, type, index):
    reportList = ReportService.getReportByStuId(stuid)
    teachingIds = []
    for i in range(len(reportList)):
        if i >= len(reportList):
            break
        teachingIds.append(reportList[i].teachingid)
    try:
        teachinglist = Teaching.objects.filter(id__in=teachingIds, status=type, isdelete=CONSTANTS.ISDELETE_NOT).all()
    except:
        return None
    else:
        teachingDictList = []
        for teaching in teachinglist:
            teachingDict = {
                "id": teaching.id,
                "experimentid": teaching.experimentid,
                "deadline": teaching.deadline,
                "teacherid": teaching.teacherid,
                "point": teaching.point,
                "remark": teaching.remark,
                "dataurl": teaching.dataurl,
                "stulisturl": teaching.stulisturl,
                "templateid": teaching.templateid,
                "videos": teaching.videos,
                "status": teaching.status,
                "isdelete": teaching.isdelete,
                "createtime": teaching.createtime,
                "updatetime": teaching.updatetime,
            }
            experiment = ExperimentService.getExperimentById(teaching.experimentid)
            teachingDict["f_experiment_name"] = experiment.name
            teachingDict["f_experiment_desc"] = experiment.desc
            teachingDict["f_experiment_url"] = experiment.url
            teacher = TeacherService.getTeacherById(teaching.teacherid)
            teachingDict["f_teacher_name"] = teacher.name
            teachingDict["f_teacher_id"] = teacher.id
            videoids = teaching.videos.split(",")
            videos = []
            for id in videoids:
                video = VideoService.getVideoById(id)
                video.url = "/getVideoById/?videourl=" + video.url
                videoobj = {
                    "url": video.url,
                    "name": video.name
                }
                videos.append(videoobj)
            teachingDict["videos"] = json.dumps(videos)
            for report in reportList:
                if report.teachingid == teaching.id:
                    teachingDict["f_report_status"] = report.status
                    teachingDict["f_report_id"] = report.id
                    if (report.url is None) or (report.url == "") or report.url == "none":
                        teachingDict["f_report_url"] = ""
                    else:
                        teachingDict["f_report_url"] = report.url
                    if report.score > 0:
                        teachingDict["f_score"] = report.score
                    else:
                        teachingDict["f_score"] = 0
            teachingDictList.append(teachingDict)
        return teachingDictList


# 获得此学生id特定类型的报告总数
def getCountPageByStu(stuid, type):
    reportList = ReportService.getReportByStuId(stuid)

    teachingIds = []

    for i in range(len(reportList)):
        if i >= len(reportList):
            break
        teachingIds.append(reportList[i].teachingid)
    if teachingIds.__len__() == 0:
        return 0

    count = Teaching.objects.filter(id__in=teachingIds, status=type, isdelete=CONSTANTS.ISDELETE_NOT).count()
    return count


# 获得此教师特定类型的报告总数
def getCountPageByTea(teaid, type):
    try:
        count = Teaching.objects.filter(teacherid=teaid, status=type, isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count


# 获得此教师的报告总数
def getCountByTea(teaid):
    try:
        count = Teaching.objects.filter(teacherid=teaid, isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count


# 获得此教师特定类型的报告分页
def getTeachingByTea(teaid, type, index):
    teachingsearch = Teaching.objects.filter(teacherid=teaid, status=type, isdelete=CONSTANTS.ISDELETE_NOT)
    try:
        teachinglist = teachingsearch.all()
    except:
        return None
    else:
        paginator = Paginator(teachinglist, 10)
        teachingPageList = paginator.page(index)
        teachingDictPageList = []
        for teaching in teachingPageList:
            teachingDict = {
                "id": teaching.id,
                "experimentid": teaching.experimentid,
                "deadline": teaching.deadline,
                "teacherid": teaching.teacherid,
                "point": teaching.point,
                "remark": teaching.remark,
                "dataurl": teaching.dataurl,
                "stulisturl": teaching.stulisturl,
                "templateid": teaching.templateid,
                "videos": teaching.videos,
                "status": teaching.status,
                "isdelete": teaching.isdelete,
                "createtime": teaching.createtime,
                "updatetime": teaching.updatetime

            }
            experiment = ExperimentService.getExperimentById(teaching.experimentid)
            teachingDict["f_experiment_name"] = experiment.name
            teachingDict["f_experiment_desc"] = experiment.desc
            teachingDict["f_experiment_url"] = experiment.url
            teacher = TeacherService.getTeacherById(teaching.teacherid)
            teachingDict["f_teacher_name"] = teacher.name
            teachingDict["f_teacher_id"] = teacher.id
            videoids = teaching.videos.split(",")
            videos = []
            for id in videoids:
                video = VideoService.getVideoById(id)
                video.url = "/getVideoById/?videourl=" + video.url
                videoobj = {
                    "id": video.id,
                    "url": video.url,
                    "name": video.name
                }
                videos.append(videoobj)
            teachingDict["videos"] = json.dumps(videos)
            stuCount = ReportService.getCountStuByTeachingid(teaching.id)
            teachingDict["stuCount"] = stuCount
            complapprepcount = ReportService.getCountStuByTeachingidAndStatus(teaching.id,
                                                                              CONSTANTS.REPORT_STATUS_SCORE)
            submitcount = ReportService.getCountStuByTeachingidAndStatus(teaching.id,
                                                                         CONSTANTS.REPORT_STATUS_SUBMIT)
            teachingDict["complapprepcount"] = complapprepcount
            if complapprepcount == stuCount:
                teachingDict["f_report_status"] = 2
            else:
                teachingDict["f_report_status"] = 1
            teachingDictPageList.append(teachingDict)
        return teachingDictPageList


# 上传实验数据
def uploadData(teachingid, dataurl):
    now = utils.getNow()
    try:
        teaching = Teaching.objects.filter(id=teachingid).update(dataurl=dataurl, updatetime=now)
    except:
        return None
    else:
        return teaching


# 上传模板
def uploadTemplate(teachingid, templateid):
    now = utils.getNow()
    try:
        teaching = Teaching.objects.filter(id=teachingid).update(templateid=templateid, updatetime=now)
    except:
        return None
    else:
        return teaching


# 删除实验教学
def deleteTeachingByid(teachingid):
    try:
        teaching = Teaching.objects.filter(id=teachingid).update(isdelete=CONSTANTS.ISDELETE_YES)
    except:
        return None
    else:
        return teaching


# 更新实验教学预习视频
def updateTeachingVideoById(teachingid, videos):
    now = utils.getNow()
    try:
        teaching = Teaching.objects.filter(id=teachingid).update(videos=videos, updatetime=now)
    except:
        return None
    else:
        return teaching


# 更新实验教学报告提交日期
def updateTeachingDeadlineById(teachingid, deadline):
    now = utils.getNow()
    if now > deadline:
        status = CONSTANTS.TEACHING_IS_STOP
    else:
        status = CONSTANTS.TEACHING_IS_RUNNING
    try:
        teacher = Teaching.objects.filter(id=teachingid).update(deadline=deadline, status=status, updatetime=now)
    except:
        return None
    else:
        return teacher


# 更新实验教学报告提交日期
def updateTeachingPointById(teachingid, point):
    now = utils.getNow()
    try:
        teacher = Teaching.objects.filter(id=teachingid).update(point=point, updatetime=now)
    except:
        return None
    else:
        return teacher


# 添加实验教学
def addTeaching(experimentid, deadline, teacherid, point, remark, dataurl, stulisturl, templateid, videos):
    now = utils.getNow()
    teaching = Teaching(experimentid=experimentid, deadline=deadline, teacherid=teacherid, point=point, remark=remark,
                        dataurl=dataurl, stulisturl=stulisturl, templateid=templateid, videos=videos,
                        status=CONSTANTS.TEACHING_IS_RUNNING, isdelete=CONSTANTS.ISDELETE_NOT, createtime=now,
                        updatetime=now)
    teaching.save()
    return teaching.id
