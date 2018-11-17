import json
from __future__ import unicode_literals


class Report(object):
    def __init__(self):
        self.__f_id = None
        self.__f_stu_id = None
        self.__f_teaching_id = None
        self.__f_url = None
        self.__f_score = None
        self.__f_is_delete = None
        self.__f_createtime = None
        self.__f_updatetime = None
        pass

    def get_f_id(self):
        return self.__f_id

    def set_f_id(self, f_id):
        self.__f_id = f_id

    def get_f_stu_id(self):
        return self.__f_stu_id

    def set_f_stu_id(self, f_stu_id):
        self.__f_stu_id = f_stu_id

    def get_f_teaching_id(self):
        return self.__f_teaching_id

    def set_f_teaching_id(self, f_teaching_id):
        self.__f_teaching_id = f_teaching_id

    def get_f_url(self):
        return self.__f_url

    def set_f_url(self, f_url):
        self.__f_url = f_url

    def get_f_score(self):
        return self.__f_score

    def set_f_score(self, f_score):
        self.__f_score = f_score

    def get_f_is_delete(self):
        return self.__f_is_delete

    def set_f_is_delete(self, f_is_delete):
        self.__f_is_delete = f_is_delete

    def get_f_createtime(self):
        return self.__f_createtime

    def set_f_createtime(self, f_createtime):
        self.__f_createtime = f_createtime

    def get_f_updatetime(self):
        return self.__f_updatetime

    def set_f_updatetime(self, f_updatetime):
        self.__f_updatetime = f_updatetime

    def __str__(self):
        reportDict = {'f_id': self.__f_id, 'f_stu_id': self.__f_stu_id, 'f_teaching_id': self.__f_teaching_id,
                      'f_url': self.__f_url, 'f_score': self.__f_score, 'f_is_delete': self.__f_is_delete,
                      'f_createtime': self.__f_createtime, 'f_updatetime': self.__f_updatetime}
        return json.dumps(reportDict, ensure_ascii=False)
