from django.db import models
import django.utils.timezone as timezone

'''
'''


class Experiment(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    name = models.CharField(max_length=50, db_column="f_name")
    desc = models.CharField(max_length=255, db_column="f_desc")
    videos = models.CharField(max_length=50, db_column="f_videos")
    url = models.CharField(max_length=50, db_column="f_url")
    templateid = models.CharField(max_length=50, db_column="f_template_id")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_experiment"


class Student(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    name = models.CharField(max_length=50, db_column="f_name")
    number = models.CharField(max_length=50, db_column="f_number")
    filterinfoid = models.IntegerField(db_column="f_filterinfo_id")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_student"


class FilterInfo(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    registyear = models.CharField(max_length=50, db_column="f_regist_year")
    major = models.CharField(max_length=50, db_column="f_major")
    classname = models.CharField(max_length=50, db_column="f_class_name")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_filterinfo"


class Teacher(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    name = models.CharField(max_length=50, db_column="f_name")
    number = models.CharField(max_length=50, db_column="f_number")
    password = models.CharField(max_length=100, db_column="f_password")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_teacher"


class Admin(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    teacherid = models.IntegerField(db_column="f_teacher_id")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_admin"


class Teaching(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    experimentid = models.IntegerField(db_column="f_experiment_id")
    deadline = models.DateTimeField(db_column="f_deadline")
    teacherid = models.IntegerField(db_column="f_teacher_id")
    point = models.CharField(max_length=255, db_column="f_point")
    remark = models.CharField(max_length=255, db_column="f_remark")
    dataurl = models.CharField(max_length=255, db_column="f_data_url")
    stulisturl = models.CharField(max_length=255, db_column="f_stulist_url")
    templateid = models.IntegerField(db_column="f_template_id")
    videos = models.CharField(max_length=255, db_column="f_videos")
    status = models.IntegerField(db_column="f_status", default=0)
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_teaching"


class Report(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    stuid = models.IntegerField(db_column="f_stu_id")
    teachingid = models.IntegerField(db_column="f_teaching_id")
    url = models.CharField(max_length=50, db_column="f_url")
    score = models.IntegerField(db_column="f_score")
    status = models.IntegerField(default=0, db_column="f_status")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_report"


class Template(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    experimentid = models.IntegerField(db_column="f_experiment_id")
    url = models.CharField(max_length=255, db_column="f_url")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_template"


class Video(models.Model):
    id = models.AutoField(primary_key=True, db_column="f_id")
    name = models.CharField(max_length=255, db_column="f_name")
    url = models.CharField(max_length=255, db_column="f_url")
    experimentid = models.IntegerField(db_column="f_experiment_id")
    isdelete = models.BooleanField(default=False, db_column="f_is_delete")
    createtime = models.DateTimeField(default=timezone.now, db_column="f_createtime")
    updatetime = models.DateTimeField(default=timezone.now, db_column="f_updatetime")

    class Meta:
        db_table = "t_video"
