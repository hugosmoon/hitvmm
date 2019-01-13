from vm4.context import CONSTANTS
from vm4.view import utils
from vm4.models import *
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


def getFilterInfoList(ids):
    try:
        filterinfo = FilterInfo.objects.order_by('registyear').order_by('major').order_by('classname').get(id__in=ids)
    except:
        return None
    else:
        return filterinfo
