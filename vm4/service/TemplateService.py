# -*- coding: UTF-8 -*-
from vm4.dao.TemplateDao import getTemplateDao
from vm4.view import utils
from vm4.context import CONSTANTS

#根据id获得模板
def getTemplateById(id):
    templateDao = getTemplateDao()
    filters = {
        "f_id": id
    }
    return templateDao.select_one(None, filters)

#添加模板
def addTemplate(experimentid, templateurl):
    templateDao = getTemplateDao()
    timenow = utils.getNowStr()
    template = {
        "f_experiment_id": experimentid,
        "f_url":templateurl,
        "f_is_delete": CONSTANTS.ISDELETE_NOT,
        "f_createtime":timenow,
        "f_updatetime":timenow,
    }
    resulttuple = templateDao.save(None,template)
    return resulttuple[0][0]