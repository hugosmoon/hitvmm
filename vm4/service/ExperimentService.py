# -*- coding: UTF-8 -*-
from vm4.service import VideoService
import json
from vm4.models import *
from vm4.context import CONSTANTS
from vm4.view import utils
from django.forms.models import model_to_dict

def getAllExperiment():
    try:
        experimentlist = Experiment.objects.all()
    except:
        return None
    else:
        experimentDictList = []
        for experiment in experimentlist:
            experimentDict = {
                "id": experiment.id,
                "name": experiment.name,
                "desc": experiment.desc,
                "videos": experiment.videos,
                "url": experiment.url,
                "templateid": experiment.templateid,
                "isdelete": experiment.isdelete,
                "createtime": experiment.createtime,
                "updatetime": experiment.updatetime
            }
            videoids = experiment.videos.split(",")
            videos = []
            for id in videoids:
                video = VideoService.getVideoById(id)
                video.url = "/getVideoById/?videourl=" + video.url
                videoobj = {
                    "id": id,
                    "url": video.url,
                    "name": video.name
                }
                videos.append(videoobj)
            experimentDict["videos"] = json.dumps(videos)
            experimentDictList.append(experimentDict)

        return experimentDictList


def getExperimentById(expId):
    try:
        experiment = Experiment.objects.filter(id=expId, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return experiment


def updateExperimentVideos(experimentid, videos):
    now = utils.getNow()
    try:
        experiment = Experiment.objects.filter(id=experimentid).update(videos=videos, updatetime=now)
    except:
        return None
    else:
        return experiment


def updateExperimentTamplate(experimentid, templateid):
    now = utils.getNow()
    try:
        experiment = Experiment.objects.filter(id=experimentid).update(templateid=templateid, updatetime=now)
    except:
        return None
    else:
        return experiment
# 更新实验描述
def updateExperimentdescription(experimentid,experimentdescription):
    now = utils.getNow()
    try:
        experiment = Experiment.objects.filter(id=experimentid).update(desc=experimentdescription, updatetime=now)
    except:
        return None
    else:
        return True