# -*- coding: UTF-8 -*-
import datetime
from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.service import StudentService
from vm4.models import *
from django.forms.models import model_to_dict

# 根据报告id获取报告
def getReportById(reportid):
    try:
        report = Report.objects.get(id=reportid)
    except:
        return None
    else:
        return report


# 根据学生id获取报告列表
def getReportByStuId(stuId):
    try:
        reportList = Report.objects.all().filter(stuid=stuId)
    except:
        return None
    else:
        return reportList


# 根据实验教学id获取报告列表
def getReportByTeachingid(teachingid):
    try:
        reportList = Report.objects.filter(teachingid=teachingid).order_by("createtime").all()
    except:
        return None
    else:
        reportDictList = []
        for report in reportList:
            reportDict = {
                "id": report.id,
                "stuid": report.stuid,
                "teachingid": report.teachingid,
                "url": report.url,
                "score": report.score,
                "status": report.status,
                "isdelete": report.isdelete,
                "createtime": report.createtime,
                "updatetime": report.updatetime
            }
            student = StudentService.getStudentById(report.stuid)
            reportDict["stuname"] = student.name
            reportDict["stunumber"] = student.number
            reportDictList.append(reportDict)
        return reportDictList


# 根据实验教学id获取学生总数
def getCountStuByTeachingid(teachingid):
    try:
        count = Report.objects.filter(teachingid=teachingid, isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count


# 根据实验教学id和实验教学状态获取学生总数
def getCountStuByTeachingidAndStatus(teachingid, status):
    try:
        count = Report.objects.filter(teachingid=teachingid, status=status, isdelete=CONSTANTS.ISDELETE_NOT).count()
    except:
        return 0
    else:
        return count


# 提交报告
def submintReport(reportid, filename):
    report = Report.objects.filter(id=reportid, status=CONSTANTS.REPORT_STATUS_PENDING).update(url=filename,
                                                                                               updatetime=utils.getNow())
    return report


# 批阅报告
def scoreReport(reportid, score):
    report = Report.objects.filter(id=reportid).update(score=score, status=CONSTANTS.REPORT_STATUS_SCORE,
                                                       updatetime=utils.getNow())
    return report


# 添加报告
def addReport(teachingid, stunid):
    now = utils.getNow()
    report = Report(stuid=stunid, teachingid=teachingid, score=0, status=CONSTANTS.REPORT_STATUS_PENDING,
                    isdelete=CONSTANTS.ISDELETE_NOT, createtime=now, updatetime=now)
    report.save()
    return report.id
