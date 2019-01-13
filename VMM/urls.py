#-*- coding: UTF-8 -*-
"""VMM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add experiment URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add experiment URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add experiment URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from vm4.view import view_student
from vm4.view import view_teacher
from vm4.view import view_admin
from vm4.view import view_experiment
urlpatterns = [
    #student
    url(r'login/$', view_student.v_login),
    url(r'login/stu/', view_student.stulogin),
    url(r'index/', view_student.v_index),
    url(r'completedexp/', view_student.v_completedexp),
    url(r'allexp/$', view_student.v_allexperiment),
    url(r'submitReport/', view_student.submitReport),
    url(r'downloaddata/', view_student.downloadData),
    url(r'downloadtemplate/', view_student.downloadTemplate),

    #teacher
    url(r'loginteacher/$', view_teacher.v_login),
    url(r'login/teacher/', view_teacher.teacherlogin),
    url(r'password/$', view_teacher.v_password),
    url(r'passwordedit/', view_teacher.editpassword),
    url(r'undoneteaching/', view_teacher.v_undoneteaching),
    url(r'allexptea/',view_teacher.v_allexperiment),
    url(r'uploadData/',view_teacher.uploadData),
    url(r'updateTeachingTemplate/',view_teacher.updateTeachingTemplate),
    url(r'deleteTeachingByid/',view_teacher.deleteTeachingByid),
    url(r'updateTeachingVideo/',view_teacher.updateTeachingVideo),
    url(r'updateTeachingDeadline/',view_teacher.updateTeachingDeadline),
    url(r'completedteaching/',view_teacher.v_completedteaching),
    url(r'approval/',view_teacher.v_approval),
    url(r'downloadStudentList/',view_teacher.downloadStudentList),
    url(r'downloadReport/',view_teacher.downloadReport),
    url(r'scoreReport/',view_teacher.scoreReport),
    url(r'addexp/$',view_teacher.v_addexp),
    url(r'addexperiment/',view_teacher.addexperiment),
    url(r'getVideoById/',view_teacher.getVideoById),
    url(r'downloadReportScoreList/',view_teacher.downloadReportScoreList),
    url(r'uploadVideo/',view_teacher.uploadVideo),
    url(r'updateExperimentVideo/',view_teacher.updateExperimentVideo),
    url(r'updateExperimentTemplate/',view_teacher.updateExperimentTemplate),




    #admin
    url(r'loginadmin/$', view_admin.v_login),
    url(r'login/admin/', view_admin.adminlogin),
    url(r'studentmanagement/', view_admin.v_studentmanagement),
    url(r'adminmanagement/', view_admin.v_adminmanagement),
    url(r'teachermanagement/', view_admin.v_teachermanagement),
    url(r'deleteStudentByid/', view_admin.deleteStudentByid),
    url(r'deleteTeacherByid/', view_admin.deleteTeacherByid),
    url(r'deleteAdminByid/', view_admin.deleteAdminByid),
    url(r'adduser/', view_admin.v_adduser),
    url(r'resetteacherpwd/', view_admin.resetTeacherPwd),
    url(r'addStudent/', view_admin.addStudent),
    url(r'addTeacher/', view_admin.addTeacher),
    url(r'addAdmin/', view_admin.addAdmin),
    url(r'getlisttemplate/', view_admin.getListTemplate),
    url(r'setBasicInformation/', view_admin.setBasicInformation),
    url(r'addFilterInfo/',view_admin.addFilterInfo),
    url(r'delFilterInfo/',view_admin.delFilterInfo),


    #experiment
    url(r'experiment/experiment1/',view_experiment.experiment1),
    url(r'experiment/experiment2/',view_experiment.experiment2),
    url(r'experiment/experiment3/',view_experiment.experiment3),
    url(r'experiment/experiment4/',view_experiment.experiment4),
    # url(r'experiment/expoperation/',view_experiment.expoperation,name='expoperation'),
    url(r'experiment/expoperation2/',view_experiment.expoperation2),
    # url(r'experiment/expsetting/',view_experiment.expsetting),
    url(r'experiment/expsetting2/',view_experiment.expsetting2),


    #experiment
    url(r'experiment/expsetting/(?P<id>[0-9]+)$',view_experiment.expsetting,name='expsetting'),
    url(r'experiment/expoperation/(?P<id>[0-9]+)$', view_experiment.expoperation,name='expoperation'),
    url(r'experiment/image_draw/', view_experiment.image_draw,name='image_draw'),

    #实现切削力计算
    url(r'experiment/cutting_force_cal/',view_experiment.cutting_force_cal,name='cutting_force_cal'),
    #实现切削温度计算
    url(r'experiment/cutting_temp_cal/',view_experiment.cutting_temp_cal,name='cutting_temp_cal'),
    #实现表面粗糙度计算
    url(r'experiment/cutting_roughness_cal/',view_experiment.cutting_roughness_cal,name='cutting_roughness_cal'),
]

