# -*- coding: UTF-8 -*-
from vm4.dao.VideoDao import getVideoDao


# 根据id列表获取视频
def getVideoByIds(ids):
    videoDao = getVideoDao()
    filters = {
        "_in_f_id": ids
    }
    return videoDao.select_all(None, filters)


# 根据id获取视频
def getVideoById(id):
    videoDao = getVideoDao()
    return videoDao.select_pk(None, primary_key=id)
