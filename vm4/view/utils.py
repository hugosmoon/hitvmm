# -*- coding:UTF-8 -*-
import datetime


def getParam(request, name):
    if request.method == 'GET':
        return request.GET.get(name, '')
    else:
        return request.POST.get(name, '')


def getCookie(request, name):
    value = request.COOKIES.get(name)
    if value is None:
        return value
    else:
        return value.encode("iso-8859-1").decode('utf8')


def setCookie(response, name, value):
    response.set_cookie(name, bytes(value, 'utf-8').decode('ISO-8859-1'), max_age=60 * 60 * 48)


def getNowStr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getNow():
    return datetime.datetime.now()
