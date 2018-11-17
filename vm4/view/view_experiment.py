# -*- coding: UTF-8 -*-
from django.shortcuts import render,HttpResponse
def experiment1(request):
    return render(request,"experiment/experiment1.html")
def experiment2(request):
    return render(request,"experiment/experiment2.html")
def experiment3(request):
    return render(request,"experiment/experiment3.html")
def experiment4(request):
    return render(request,"experiment/experiment4.html")