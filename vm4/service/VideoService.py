# -*- coding: UTF-8 -*-
from vm4.view import utils
from vm4.context import CONSTANTS
from vm4.models import *
from django.forms.models import model_to_dict

# 根据id列表获取视频
def getVideoByIds(ids):
    try:
        videos = Video.objects.filter(id__in=ids, isdelete=CONSTANTS.ISDELETE_NOT).all()
    except:
        return None
    else:
        videos


# 根据id获取视频
def getVideoById(id):
    try:
        video = Video.objects.filter(id=id, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return video


def saveVideo(name, url, experimentid):
    now = utils.getNow()
    video = Video(name=name, url=url, experimentid=experimentid, isdelete=CONSTANTS.ISDELETE_NOT, createtime=now,
                  updatetime=now)
    video.save()
    return video.id
