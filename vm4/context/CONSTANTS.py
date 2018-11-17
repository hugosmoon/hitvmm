#-*- coding: UTF-8 -*-

'''
    常量类
'''

DEFUALT_PASSWORD="1234"

#是否删除
ISDELETE_NOT = 0
ISDELETE_YES = 1

#实验教学是否开启
TEACHING_IS_RUNNING = 0
TEACHING_IS_STOP = 1

#实验数据存放路径前缀
DATAURL_PRE = "/usr/local/vmmfile/experimentaldata/"
#实验报告模板存放路径前缀
TEMPLATEURL_PRE = "/usr/local/vmmfile/experimenttemplate/"
#实验报告存放路径前缀
REPORTURL_PRE = "/usr/local/vmmfile/report/"
#学生列表存放路径前缀
STUDENTLISTURL_PRE = "/usr/local/vmmfile/studentlist/"
#添加用户模板路径前缀
ADDUSERTEMPLATEURL_PRE = "/usr/local/vmmfile/listtemplate/"
#实验视频路径前缀
EXPERIMENTVIDEOURL_PRE = "/usr/local/vmmfile/video/"
#学生成绩路径前缀
REPORTSCOREURL_PRE = "/usr/local/vmmfile/reportscore/"

#实验报告状态
#状态（0：待提交，1：已提交，2：已批阅）
REPORT_STATUS_PENDING = 0
REPORT_STATUS_SUBMIT = 1
REPORT_STATUS_SCORE = 2

#添加用户类型
ADD_USER_TYPE_STUDENT = "1"
ADD_USER_TYPE_TEACHER = "2"
ADD_USER_TYPE_ADMIN = "3"
