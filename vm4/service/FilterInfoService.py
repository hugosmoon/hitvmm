from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.models import *
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


def getFilterInfoList(ids):
    try:
        if ids is None:
            filterinfolist = FilterInfo.objects.order_by('-registyear', '-major', 'classname').filter(
                isdelete=CONSTANTS.ISDELETE_NOT).all()

        else:
            filterinfolist = FilterInfo.objects.order_by('-registyear', '-major', 'classname').filter(
                isdelete=CONSTANTS.ISDELETE_NOT, id__in=ids).all()
    except:
        return None
    else:
        return filterinfolist

#教研是否存在
def getFilterInfo(registyear, major, classname):
    try:
        filterinfo = FilterInfo.objects.filter(isdelete=CONSTANTS.ISDELETE_NOT, registyear=registyear, major=major,
                                               classname=classname).get()
    except:
        return None
    else:
        return filterinfo


def addFilterInfo(registyear, major, classname):
    now = utils.getNow()
    filterinfo = FilterInfo(registyear=registyear, major=major, classname=classname, isdelete=CONSTANTS.ISDELETE_NOT,
                            createtime=now, updatetime=now)
    filterinfo.save()
    return filterinfo.id

#通过filterid查询filter信息
def getFilterInfoById(filterid):
    try:
        filterinfo = FilterInfo.objects.filter(id=filterid, isdelete=CONSTANTS.ISDELETE_NOT).get()
    except:
        return None
    else:
        return filterinfo


def delFilterInfo(filterid):
    try:
        filterinfo = FilterInfo.objects.filter(id=filterid, isdelete=CONSTANTS.ISDELETE_NOT).update(
            isdelete=CONSTANTS.ISDELETE_YES)
    except:
        return None
    else:
        return filterinfo
