# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def page_not_found(request, exception):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')

