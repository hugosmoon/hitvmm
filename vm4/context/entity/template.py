from __future__ import unicode_literals
import json


class Template(object):
    def __init__(self):
        self.__f_id = None
        self.__f_experiment_id = None
        self.__f_url = None
        self.__f_is_delete = None
        self.__f_createtime = None
        self.__f_updatetime = None
        pass

    def get_f_id(self):
        return self.__f_id

    def set_f_id(self, f_id):
        self.__f_id = f_id

    def get_f_experiment_id(self):
        return self.__f_experiment_id

    def set_f_experiment_id(self, f_experiment_id):
        self.__f_experiment_id = f_experiment_id

    def get_f_url(self):
        return self.__f_url

    def set_f_url(self, f_url):
        self.__f_url = f_url

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
        templateDict = {'f_id': self.__f_id, 'f_experiment_id': self.__f_experiment_id, 'f_url': self.__f_url,
                        'f_is_delete': self.__f_is_delete, 'f_createtime': self.__f_createtime,
                        'f_updatetime': self.__f_updatetime}
        return json.dumps(templateDict, ensure_ascii=False)
