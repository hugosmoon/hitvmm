# -*- coding: UTF-8 -*-
from vm4.dao.ExperimentDao import getExperimentDao
from vm4.service import VideoService
import json


def getAllExperiment():
    experimentDao = getExperimentDao()
    experimentlist = experimentDao.select_all(None)
    for experiment in experimentlist:
        videoids = experiment["f_videos"].split(",")
        videos = []
        for id in videoids:
            video = VideoService.getVideoById(id)
            video["f_url"] = "/getVideoById/?videourl=" + video["f_url"]
            videoobj = {
                "url": video["f_url"],
                "name": video["f_name"]
            }
            videos.append(videoobj)
        experiment["videos"] = json.dumps(videos)

    return experimentlist


def getExperimentById(expId):
    experimentDao = getExperimentDao()
    filters = {
        "f_id": expId
    }
    return experimentDao.select_one(None, filters)
