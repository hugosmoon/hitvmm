import json
from __future__ import unicode_literals


class Admin(object):
    def __init__(self):
        self.__f_id = None
        self.__f_teacher_number = None
        self.__f_teacher_id = None
        self.__f_is_delete = None
        self.__f_createtime = None
        self.__f_updatetime = None
        pass

    def get_f_id(self):
        return self.__f_id

    def set_f_id(self, f_id):
        self.__f_id = f_id

    def get_f_teacher_number(self):
        return self.__f_teacher_number

    def set_f_teacher_number(self, f_teacher_number):
        self.__f_teacher_number = f_teacher_number

    def get_f_teacher_id(self):
        return self.__f_teacher_id

    def set_f_teacher_id(self, f_teacher_id):
        self.__f_teacher_id = f_teacher_id

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
        adminDict = {'f_id': self.__f_id, 'f_teacher_number': self.__f_teacher_number,
                     'f_teacher_id': self.__f_teacher_id, 'f_is_delete': self.__f_is_delete,
                     'f_createtime': self.__f_createtime, 'f_updatetime': self.__f_updatetime}
        return json.dumps(adminDict, ensure_ascii=False)
