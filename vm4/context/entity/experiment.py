import json
from __future__ import unicode_literals


class Experiment(object):
    def __init__(self):
        self.__f_id = None
        self.__f_name = None
        self.__f_desc = None
        self.__f_videos = None
        self.__f_url = None
        self.__f_template = None
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

    def get_f_desc(self):
        return self.__f_desc

    def set_f_desc(self, f_desc):
        self.__f_desc = f_desc

    def get_f_videos(self):
        return self.__f_videos

    def set_f_videos(self, f_videos):
        self.__f_videos = f_videos

    def get_f_url(self):
        return self.__f_url

    def set_f_url(self, f_url):
        self.__f_url = f_url

    def get_f_template(self):
        return self.__f_template

    def set_f_template(self, f_template):
        self.__f_template = f_template

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
        experimentDict = {'f_id': self.__f_id, 'f_name': self.__f_name, 'f_desc': self.__f_desc,
                          'f_videos': self.__f_videos, 'f_url': self.__f_url, 'f_template': self.__f_template,
                          'f_is_delete': self.__f_is_delete, 'f_createtime': self.__f_createtime,
                          'f_updatetime': self.__f_updatetime}
        return json.dumps(experimentDict, ensure_ascii=False)
