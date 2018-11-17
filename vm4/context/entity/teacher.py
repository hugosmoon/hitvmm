from __future__ import unicode_literals
import json


class Teacher(object):
    def __init__(self):
        self.__f_id = None
        self.__f_name = None
        self.__f_number = None
        self.__f_password = None
        self.__f_is_delete = None
        self.__f_createtime = None
        self.__f_updatetime = None
        pass

    def get_f_id(self):
        return self.__f_id

    def set_f_id(self, f_id):
        self.__f_id = f_id

    def get_f_name(self):
        return self.__f_name

    def set_f_name(self, f_name):
        self.__f_name = f_name

    def get_f_number(self):
        return self.__f_number

    def set_f_number(self, f_number):
        self.__f_number = f_number

    def get_f_password(self):
        return self.__f_password

    def set_f_password(self, f_password):
        self.__f_password = f_password

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
        teacherDict = {'f_id': self.__f_id, 'f_name': self.__f_name, 'f_number': self.__f_number,
                       'f_password': self.__f_password, 'f_is_delete': self.__f_is_delete,
                       'f_createtime': self.__f_createtime, 'f_updatetime': self.__f_updatetime}
        return json.dumps(teacherDict, ensure_ascii=False)
    def getdict(self):
        teacherDict = {'f_id': self.__f_id, 'f_name': self.__f_name, 'f_number': self.__f_number,
                       'f_password': self.__f_password, 'f_is_delete': self.__f_is_delete,
                       'f_createtime': self.__f_createtime, 'f_updatetime': self.__f_updatetime}
        return teacherDict
