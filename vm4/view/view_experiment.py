# -*- coding: UTF-8 -*-
from django.shortcuts import render,HttpResponse
import math
import random

from vm4.service import StudentService

from django.shortcuts import render
from django.shortcuts import HttpResponse

from vm4.view import utils



def experiment1(request):
    return render(request,"experiment/experiment1.html")
def experiment2(request):
    return render(request,"experiment/experiment2.html")
def experiment3(request):
    return render(request,"experiment/experiment3.html")
def experiment4(request):
    return render(request,"experiment/experiment4.html")
def expoperation(request):
    return render(request, "experiment/experiment1/expoperation.html")
def expoperation2(request):
    return render(request,"experiment/expoperation2.html")
def expsetting(request,id):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    stuname = utils.getCookie(request, "stuname")
    stunumber = StudentService.getStudentById(stuid).number
    if id == '1':
        return render(request, "experiment/experiment1/expsetting.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '2':
        return render(request, "experiment/experiment2/expsetting.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '3':
        return render(request, "experiment/experiment3/expsetting.html"),{"stuname": stuname,"stunumber":stunumber}
    elif id == '4':
        return render(request, "experiment/experiment4/expsetting.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '5':
        return render(request, "experiment/experiment5/expsetting.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '6':
        return render(request, "experiment/experiment6/expsetting.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '7':
        return render(request, "experiment/experiment7/expsetting.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '8':
        return render(request, "experiment/experiment8/expsetting.html",{"stuname": stuname,"stunumber":stunumber})

def expsetting2(request):
    return render(request,"experiment/expsetting2.html")

def expoperation(request,id):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    stuname = utils.getCookie(request, "stuname")
    stunumber = StudentService.getStudentById(stuid).number
    if id == '1':
        return render(request, "experiment/experiment1/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id=='2':
        return render(request, "experiment/experiment2/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id=='3':
        return render(request, "experiment/experiment3/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id=='4':
        return render(request, "experiment/experiment4/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '5':
        return render(request, "experiment/experiment5/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '6':
        return render(request, "experiment/experiment6/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '7':
        return render(request, "experiment/experiment7/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '8':
        return render(request, "experiment/experiment8/expoperation.html",{"stuname": stuname,"stunumber":stunumber})
    elif id == '9':
        return render(request, "experiment/experiment9/expoperation.html",{"stuname": stuname,"stunumber":stunumber})

def image_draw(request):
    stuid = utils.getCookie(request, "stuid")
    if (stuid is None) or stuid == "":
        return getloginResponse(request)
    stuname = utils.getCookie(request, "stuname")
    stunumber = StudentService.getStudentById(stuid).number
    return render(request,"experiment/image_draw.html",{"stuname": stuname,"stunumber":stunumber})


# 计算切削力

def cutting_force_cal(request):
    #接收基础参数
    if request.method == 'POST':
        workpiece_material=request.POST.get('workpiece_material')
        feed_rate = float(request.POST.get('feed_rate'))
        cutting_depth = float(request.POST.get('cutting_depth'))
        cutting_speed = float(request.POST.get('cutting_speed'))
        tool_cutting_edge_angle = (request.POST.get('tool_cutting_edge_angle'))
        rake_angle = (request.POST.get('rake_angle'))
        tool_cutting_edge_inclination_angle = (request.POST.get('tool_cutting_edge_inclination_angle'))
        corner_radius = (request.POST.get('corner_radius'))


    else:
        return HttpResponse(False)



    #定义各种参数
    c_fc=x_fc=y_fc=k_tool_cutting_edge_angle=k_rake_angle=k_tool_cutting_edge_inclination_angle=k_corner_radius=k_strength=0
    k_cutting_speed=1

    #依据工件材料修改参数
    if(workpiece_material=="45_steel"):
        c_fc = 180
        x_fc = 1.0
        y_fc = 0.75
        k_strength=1
        if(float(cutting_speed)<17):
            k_cutting_speed=1-(0.2/17)*float(cutting_speed)
        elif(float(cutting_speed)>=17 and float(cutting_speed)<30):
            k_cutting_speed = 0.8 + (0.4/ 13) * (float(cutting_speed)-17)
        elif(float(cutting_speed)>=30 and float(cutting_speed)<40):
            k_cutting_speed=1.2-(float(cutting_speed)-30)*(0.2/10)
        elif(float(cutting_speed)>=40 and float(cutting_speed)<800):
            k_cutting_speed = 1 - (float(cutting_speed) - 40) * (0.2/760)
        elif(float(cutting_speed)>=1000):
            k_cutting_speed=0.8

    elif(workpiece_material=="stainless_steel"):
        c_fc = 204
        x_fc = 1.0
        y_fc = 0.75
        k_strength = 1
    elif (workpiece_material == "gray_iron"):
        c_fc = 92
        x_fc = 1.0
        y_fc = 0.75
        k_strength = 1
    elif (workpiece_material == "malleable_cast_iron"):
        c_fc = 81
        x_fc = 1.0
        y_fc = 0.75
        k_strength = 1

    #依据刀具角度修改参数
    #主偏角
    if(tool_cutting_edge_angle=="30"):
        k_tool_cutting_edge_angle=1.08
    elif(tool_cutting_edge_angle=="45"):
        k_tool_cutting_edge_angle=1.0
    elif(tool_cutting_edge_angle=="60"):
        k_tool_cutting_edge_angle=0.94
    elif(tool_cutting_edge_angle=="75"):
        k_tool_cutting_edge_angle=0.92
    elif (tool_cutting_edge_angle == "90"):
        k_tool_cutting_edge_angle = 0.89

    #前角
    if(rake_angle=="-15"):
        k_rake_angle=1.25
    elif(rake_angle=="-10"):
        k_rake_angle=1.2
    elif(rake_angle=="0"):
        k_rake_angle=1.1
    elif(rake_angle=="10"):
        k_rake_angle=1.0
    elif(rake_angle=="20"):
        k_rake_angle=0.9

    #刃倾角
    # if(tool_cutting_edge_inclination_angle=="5"):
    #     k_tool_cutting_edge_inclination_angle=0.75
    # elif(tool_cutting_edge_inclination_angle=="0"):
    #     k_tool_cutting_edge_inclination_angle=1.0
    # elif (tool_cutting_edge_inclination_angle == "-5"):
    #     k_tool_cutting_edge_inclination_angle = 1.25
    # elif (tool_cutting_edge_inclination_angle == "-10"):
    #     k_tool_cutting_edge_inclination_angle = 1.5
    # elif (tool_cutting_edge_inclination_angle == "-15"):
    k_tool_cutting_edge_inclination_angle = 1

    #刀尖圆弧半径
    k_corner_radius=1

    #计算切削力
    cutting_force=(random.uniform(0.9, 1.1))*9.81*c_fc*(math.pow(cutting_depth,x_fc))*(math.pow(feed_rate,y_fc))*k_tool_cutting_edge_angle*k_rake_angle*k_tool_cutting_edge_inclination_angle*k_corner_radius*k_strength*k_cutting_speed

    return HttpResponse(cutting_force)

# 计算切削温度
def cutting_temp_cal(request):
    # 接收基础参数
    if request.method == 'POST':
        workpiece_material = request.POST.get('workpiece_material')
        feed_rate = float(request.POST.get('feed_rate'))
        cutting_depth = float(request.POST.get('cutting_depth'))
        cutting_speed = float(request.POST.get('cutting_speed'))
        tool_cutting_edge_angle = (request.POST.get('tool_cutting_edge_angle'))
        rake_angle = (request.POST.get('rake_angle'))
        tool_cutting_edge_inclination_angle = (request.POST.get('tool_cutting_edge_inclination_angle'))
        corner_radius = (request.POST.get('corner_radius'))
        cutting_fluid=request.POST.get('cutting_fluid')


    else:
        return HttpResponse(False)

    #计算各种修正参数
    k0 = 220 + 0.4 * cutting_speed
    k_tool_cutting_edge_angle = 0
    k_rake_angle = 0
    k_workpiece_material = 0

    x=0.26+feed_rate*0.15
    cutting_fluid_arg=1;


    # 主偏角
    if (tool_cutting_edge_angle == "30"):
        k_tool_cutting_edge_angle = 1
    elif (tool_cutting_edge_angle == "45"):
        k_tool_cutting_edge_angle = 1.05
    elif (tool_cutting_edge_angle == "60"):
        k_tool_cutting_edge_angle = 1.15
    elif (tool_cutting_edge_angle == "75"):
        k_tool_cutting_edge_angle = 1.2
    elif (tool_cutting_edge_angle == "90"):
        k_tool_cutting_edge_angle = 1.25

    # 前角
    if (rake_angle == "-15"):
        k_rake_angle = 1.2
    elif (rake_angle == "-10"):
        k_rake_angle = 1.15
    elif (rake_angle == "0"):
        k_rake_angle = 1.1
    elif (rake_angle == "10"):
        k_rake_angle = 1.05
    elif (rake_angle == "20"):
        k_rake_angle = 1



    #根据工件材料确定参数
    if (workpiece_material == "45_steel"):
        k_workpiece_material = 1
    elif (workpiece_material == "stainless_steel"):
        k_workpiece_material = 1.3
    elif (workpiece_material == "gray_iron"):
        k_workpiece_material = 0.8
    elif (workpiece_material == "malleable_cast_iron"):
        k_workpiece_material = 0.85

    # 切削液条件
    if cutting_fluid=="water_based_cutting_fluid":
        cutting_fluid_arg=0.55
    elif cutting_fluid=="oil_based_cutting_fluid":
        cutting_fluid_arg = 0.88

    temp=(random.uniform(0.9, 1.1))*k0*k_tool_cutting_edge_angle*k_rake_angle*k_workpiece_material*math.pow(cutting_speed,x)*math.pow(cutting_depth,0.04)*math.pow(feed_rate,0.14)*cutting_fluid_arg

    return HttpResponse(temp)

#计算表面粗糙度
def cutting_roughness_cal(request):
    # 接收基础参数
    if request.method == 'POST':
        feed_rate = float(request.POST.get('feed_rate'))
        cutting_depth = float(request.POST.get('cutting_depth'))
        cutting_speed = float(request.POST.get('cutting_speed'))
        tool_cutting_edge_angle = float(request.POST.get('tool_cutting_edge_angle'))
        tool_minor_cutting_edge_angle = float(request.POST.get('tool_minor_cutting_edge_angle'))
        corner_radius = float(request.POST.get('corner_radius'))

        R=(random.uniform(1, 1.4))*(math.pow(feed_rate, 2)/(8*corner_radius))*(1/((1/(math.tan(tool_cutting_edge_angle)))+(1/(math.tan(tool_minor_cutting_edge_angle)))))*math.pow(cutting_depth, 0.04)*(1+1/(math.pow((cutting_speed-30), 2)+1))
        # R=(random.uniform(1, 1.4))*(math.pow(feed_rate, 2)/(8*corner_radius))
        # R=corner_radius

        return HttpResponse(R)

#获取登录页responsegetloginResponse
def getloginResponse(request):
    response = render(request, "login.html")
    response.delete_cookie("stuid")
    response.delete_cookie("stuname")
    response.delete_cookie("stunum")
    return response