# -*- coding: UTF-8 -*-
from vm4.dao.ReportDao import getReportDao
import datetime
from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.service import StudentService


# 根据报告id获取报告
def getReportById(reportid):
    reportDao = getReportDao()
    return reportDao.select_pk(primary_key=reportid)


# 根据学生id获取报告列表
def getReportByStuId(stuId):
    reportDao = getReportDao()
    filter = {
        "f_stu_id": stuId,
    }
    return reportDao.select_all(None, filter)


# 根据实验教学id获取报告列表
def getReportByTeachingid(teachingid):
    reportDao = getReportDao()
    filter = {
        "f_teaching_id": teachingid,
        "orderby": "f_createtime",
    }
    reportList = reportDao.select_all(None, filter)
    for report in reportList:
        student = StudentService.getStudentById(report["f_stu_id"])
        report["stuname"] = student["f_name"]
        report["stunumber"] = student["f_number"]
    return reportList


# 根据实验教学id获取学生总数
def getCountStuByTeachingid(teachingid):
    reportDao = getReportDao()
    filter = {
        "f_teaching_id": teachingid
    }
    return reportDao.count(None, filter)


# 根据实验教学id和实验教学状态获取学生总数
def getCountStuByTeachingidAndStatus(teachingid, status):
    reportDao = getReportDao()
    filter = {
        "f_teaching_id": teachingid,
        "f_status": status
    }
    return reportDao.count(None, filter)


# 根据实验教学id删除报告
def deleteReportByTeachingid(teachingids):
    reportDao = getReportDao()


# 提交报告
def submintReport(reportid, filename):
    reportDao = getReportDao()
    report = {"f_id": reportid}
    report["f_url"] = filename
    report["f_status"] = CONSTANTS.REPORT_STATUS_SUBMIT
    report["f_updatetime"] = utils.getNowStr()
    return reportDao.update_by_primarikey_selective(None, report)


# 批阅报告
def scoreReport(reportid, score):
    reportDao = getReportDao()
    report = {"f_id": reportid, "f_score": score, "f_status": CONSTANTS.REPORT_STATUS_SCORE}
    report["f_updatetime"] = utils.getNowStr()
    reportDao.update_by_primarikey_selective(None, report)


# 添加报告
def addReport(teachingid, stunid):
    reportDao = getReportDao()
    now = utils.getNowStr()
    report = {
        "f_stu_id": stunid,
        "f_teaching_id": teachingid,
        "f_createtime": now,
        "f_updatetime": now,
    }
    return reportDao.save(None, report)
