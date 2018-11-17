import json
from __future__ import unicode_literals


class Teaching(object):
    def __init__(self):
        self.__f_id = None
        self.__f_experiment_id = None
        self.__f_deadline = None
        self.__f_point = None
        self.__f_remark = None
        self.__f_data_url = None
        self.__f_stulist_url = None
        self.__f_template_id = None
        self.__f_videos = None
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

    def get_f_deadline(self):
        return self.__f_deadline

    def set_f_deadline(self, f_deadline):
        self.__f_deadline = f_deadline

    def get_f_point(self):
        return self.__f_point

    def set_f_point(self, f_point):
        self.__f_point = f_point

    def get_f_remark(self):
        return self.__f_remark

    def set_f_remark(self, f_remark):
        self.__f_remark = f_remark

    def get_f_data_url(self):
        return self.__f_data_url

    def set_f_data_url(self, f_data_url):
        self.__f_data_url = f_data_url

    def get_f_stulist_url(self):
        return self.__f_stulist_url

    def set_f_stulist_url(self, f_stulist_url):
        self.__f_stulist_url = f_stulist_url

    def get_f_template_id(self):
        return self.__f_template_id

    def set_f_template_id(self, f_template_id):
        self.__f_template_id = f_template_id

    def get_f_videos(self):
        return self.__f_videos

    def set_f_videos(self, f_videos):
        self.__f_videos = f_videos

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
        teachingDict = {'f_id': self.__f_id, 'f_experiment_id': self.__f_experiment_id, 'f_deadline': self.__f_deadline,
                        'f_point': self.__f_point, 'f_remark': self.__f_remark, 'f_data_url': self.__f_data_url,
                        'f_stulist_url': self.__f_stulist_url, 'f_template_id': self.__f_template_id,
                        'f_videos': self.__f_videos, 'f_is_delete': self.__f_is_delete,
                        'f_createtime': self.__f_createtime, 'f_updatetime': self.__f_updatetime}
        return json.dumps(teachingDict, ensure_ascii=False)
