# -*- coding:UTF-8 -*-
import datetime


def getParam(request, name):
    if request.method == 'GET':
        return request.GET.get(name, '').encode("utf-8")
    else:
        return request.POST.get(name, '').encode("utf-8")


def getCookie(request, name):
    return request.COOKIES.get(name)

def setCookie(response , name ,value):
    response.set_cookie(name, value,max_age=60*60*2)

def getNowStr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getNow():
    return datetime.datetime.now()
