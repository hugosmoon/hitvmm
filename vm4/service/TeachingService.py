# -*- coding: UTF-8 -*-
from vm4.dao.TeachingDao import getTeachingDao
from vm4.service import ReportService
from vm4.service import ExperimentService
from vm4.service import VideoService
from vm4.service import TeacherService
from vm4.view import utils
from vm4.context import CONSTANTS
from vm4.dao.baseDao.page import Page
import json


# 根据学生id获得教学
def getTeachingByStu(stuid, type, index):
    teachingDao = getTeachingDao()
    reportList = ReportService.getReportByStuId(stuid)
    teachingIds = ""
    for i in range(len(reportList)):
        if i >= len(reportList):
            break
        teachingIds = teachingIds + str(reportList[i].get("f_teaching_id"))
        if i < (len(reportList) - 1):
            teachingIds = teachingIds + ","
    filters = {
        "_in_f_id": teachingIds,
        "f_status": type,
    }
    page = Page(page_num=int(index))
    teachinglist = teachingDao.select_page(None, page, filters)
    if teachinglist is None:
        return []
    for teaching in teachinglist:
        experiment = ExperimentService.getExperimentById(teaching.get("f_experiment_id"))
        teaching["f_experiment_name"] = experiment["f_name"]
        teaching["f_experiment_desc"] = experiment["f_desc"]
        teaching["f_experiment_url"] = experiment["f_url"]
        teacher = TeacherService.getTeacherById(teaching.get("f_teacher_id"))
        teaching["f_teacher_name"] = teacher["f_name"]
        teaching["f_teacher_id"] = teacher["f_id"]
        videoids = teaching["f_videos"].split(",")
        videos = []
        for id in videoids:
            video = VideoService.getVideoById(id)
            video["f_url"] = "/getVideoById/?videourl=" + video["f_url"]
            videoobj = {
                "url":video["f_url"],
                "name":video["f_name"]
            }
            videos.append(videoobj)
        teaching["videos"] = json.dumps(videos)
        for report in reportList:
            if report["f_teaching_id"] == teaching["f_id"]:
                teaching["f_report_status"] = report["f_status"]
                teaching["f_report_id"] = report["f_id"]
                if (report["f_url"] is None) or (report["f_url"] == ""):
                    teaching["f_report_url"] = ""
                else:
                    teaching["f_report_url"] = report["f_url"]
                if report["f_score"] > 0:
                    teaching["f_score"] = report["f_score"]
                else:
                    teaching["f_score"] = 0
    return teachinglist


# 获得此学生id特定类型的报告总数
def getCountPageByStu(stuid, type):
    teachingDao = getTeachingDao()
    reportList = ReportService.getReportByStuId(stuid)
    teachingIds = ""
    for i in range(len(reportList)):
        if i >= len(reportList):
            break
        teachingIds = teachingIds + str(reportList[i].get("f_teaching_id"))
        if i < (len(reportList) - 1):
            teachingIds = teachingIds + ","
    if teachingIds == "":
        return 0
    filters = {
        "_in_f_id": teachingIds,
        "f_status": type,
    }
    count = teachingDao.count(filters=filters)
    return count


# 获得此教师特定类型的报告总数
def getCountPageByTea(teaid, type):
    teachingDao = getTeachingDao()
    filters = {
        "f_teacher_id": teaid,
        "f_status": type,
    }
    count = teachingDao.count(filters=filters)
    return count


# 获得此教师特定类型的报告分页
def getTeachingByTea(teaid, type, index):
    teachingDao = getTeachingDao()
    filters = {
        "f_teacher_id": teaid,
        "f_status": type,
    }
    page = Page(page_num=int(index))
    teachinglist = teachingDao.select_page(None, page, filters)
    if teachinglist is None:
        return []
    for teaching in teachinglist:
        experiment = ExperimentService.getExperimentById(teaching.get("f_experiment_id"))
        teaching["f_experiment_name"] = experiment["f_name"]
        teaching["f_experiment_desc"] = experiment["f_desc"]
        teaching["f_experiment_url"] = experiment["f_url"]
        teacher = TeacherService.getTeacherById(teaching.get("f_teacher_id"))
        teaching["f_teacher_name"] = teacher["f_name"]
        teaching["f_teacher_id"] = teacher["f_id"]
        stuCount = ReportService.getCountStuByTeachingid(teaching["f_id"])
        teaching["stuCount"] = stuCount
        complapprepcount = ReportService.getCountStuByTeachingidAndStatus(teaching["f_id"],
                                                                          CONSTANTS.REPORT_STATUS_SCORE)
        submitcount = ReportService.getCountStuByTeachingidAndStatus(teaching["f_id"], CONSTANTS.REPORT_STATUS_SUBMIT)
        teaching["complapprepcount"] = complapprepcount
        if submitcount > 0:
            teaching["f_report_status"] = 1
        else:
            teaching["f_report_status"] = 2
    return teachinglist


# 上传实验数据
def uploadData(teachingid, dataurl):
    teachingDao = getTeachingDao()
    teaching = {"f_id": teachingid}
    teaching["f_data_url"] = dataurl
    teaching["f_updatetime"] = utils.getNowStr()
    teachingDao.update_by_primarikey_selective(None, teaching)


# 上传模板
def uploadTemplate(teachingid, templateid):
    teachingDao = getTeachingDao()
    teaching = {"f_id": teachingid}
    teaching["f_template_id"] = templateid
    teaching["f_updatetime"] = utils.getNowStr()
    teachingDao.update_by_primarikey_selective(None, teaching)


# 删除实验教学
def deleteTeachingByid(teachingid):
    teachingDao = getTeachingDao()
    teaching = {"f_id": teachingid, "f_is_delete": CONSTANTS.ISDELETE_YES}
    teachingDao.update_by_primarikey_selective(None, teaching)


# 更新实验教学预习视频
def updateTeachingVideoById(teachingid, videos):
    teachingDao = getTeachingDao()
    teaching = {"f_id": teachingid, "f_videos": videos}
    teachingDao.update_by_primarikey_selective(None, teaching)


# 更新实验教学报告提交日期
def updateTeachingDeadlineById(teachingid, deadline):
    teachingDao = getTeachingDao()
    now = utils.getNow()
    if now > deadline:
        status = CONSTANTS.TEACHING_IS_STOP
    else:
        status = CONSTANTS.TEACHING_IS_RUNNING
    teaching = {"f_id": teachingid, "f_deadline": deadline, "f_status": status}
    teachingDao.update_by_primarikey_selective(None, teaching)


# 添加实验教学
def addTeaching(experimentid, deadline, teacherid, point, remark, dataurl, stulisturl, templateid, videos):
    teachingDao = getTeachingDao()
    now = utils.getNowStr()
    teaching = {
        "f_experiment_id": experimentid,
        "f_deadline": deadline,
        "f_teacher_id": teacherid,
        "f_point": point,
        "f_remark": remark,
        "f_data_url": dataurl,
        "f_stulist_url": stulisturl,
        "f_template_id": templateid,
        "f_videos": videos,
        "f_status": CONSTANTS.TEACHING_IS_RUNNING,
        "f_is_delete": CONSTANTS.ISDELETE_NOT,
        "f_createtime": now,
        "f_updatetime": now
    }
    teachingid = teachingDao.save(None, teaching)
    if teachingid is None:
        return None
    return teachingid[0][0]
