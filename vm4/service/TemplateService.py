# -*- coding: UTF-8 -*-
from vm4.dao.TemplateDao import getTemplateDao
from vm4.view import utils
from vm4.context import CONSTANTS
from vm4.models import *


# 根据id获得模板
def getTemplateById(id):
    try:
        template = Template.objects.filter(id=id, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return template


# 添加模板
def addTemplate(experimentid, templateurl):
    now = utils.getNow()
    template = Template(experimentid=experimentid, url=templateurl, isdelete=CONSTANTS.ISDELETE_NOT, createtime=now,
                        updatetime=now)
    template.save()
    return template.id
