var publicObj = {
    dataObjKind: 0,
    addepxupdatamodObj: '',
    addexpteastulistObj: '',
    addexpupexpdataObj: '',
    videodataObj: '',
    addvideotype: '',
    init: function () {
        //this.makeLoadDom();
        //this.makeNav()
        // this.makeTeaNav()
        this.switchNavigaTion();
        this.rotue()
        this.bindBtn()
        this.hidePopup()
        this.hack()
        this.changeVideo()
        this.radioBtn();
        this.changePreVideo()
        this.calendar();
    },
    hack: function () {
        var footerStr = '<div style="width: 100%;height: 150px"></div>'
        $('body').append(footerStr)
    },
    rotue: function () {
        $(".adduserbox").bind('click', function () {
            window.open('/adduser/')
        })
        $(".t_txt5").bind('click', function () {
            if (confirm("确认重置此教师的密码？")) {
                teacherid = $(this).attr("teacherid")
                $.post("/resetteacherpwd/",
                    {
                        teacherid: teacherid
                    },
                    function (data, status) {
                        dataObj = $.parseJSON(data)
                        code = dataObj.code;
                        if (code == -2) {//未登录
                            window.location = "/loginadmin/";
                        } else if (code != 0) {
                            alert(dataObj.desc);
                        } else {
                            alert("修改成功！")
                        }
                    });
            }
        })
        $(".adminlogin").bind('click', function () {
            var adminid = $(".iptusierid").val();
            var adminpwd = $(".iptname").val();
            $.post("/login/admin/",
                {
                    adminid: adminid,
                    adminpwd: sha256_digest(adminpwd)
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code != 0) {
                        alert(dataObj.desc);
                    } else {
                        $(location).attr('href', '/studentmanagement/');
                    }
                });
        })
        $(".changepsw").unbind("click").bind('click', function () {
            location.href = '/password/'
        })
    },
    switchNavigaTion: function () {
        $(".activearrow1").unbind("click").bind('click', function () {
            $(".navcenter1,.activearrow1").hide()
            $(".uparrow").show()
        })
        $(".uparrow").unbind("click").bind('click', function () {
            $(".uparrow").hide()
            $(".activearrow1,.navcenter1").show()
        })

        $(".activearrow2").unbind("click").bind('click', function () {
            $(".navcenter2,.activearrow2").hide()
            $(".uparrow2").show()
        })

        $(".uparrow2").unbind("click").bind('click', function () {
            $(".navcenter2,.activearrow2").show()
            $(".uparrow2").hide()
        })
    },
    //绑定事件
    bindBtn: function () {
        this.indexEvent()
        this.allexpEvent()
        this.studentmanagementEvent()
        this.teachermanagementEvent()
        this.adminmanagementEvent()
        this.changePossword()
        this.undoneteachingEvent()
        this.completedteachingEvent()
        this.allexpteaEvent()
        this.approvalEvent()
        this.adduserEvent()
    },
    adduserEvent: function () {
        $(".adduserup").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall2').show()
                $(".popupmid").hide()
                $(".popupmid3").show()
                type = $("#type").attr("attr")
                if (type == 1) {
                    $("#uploadfile").attr("action", "/addBatchStudent/")
                } else if (type == 2) {
                    $("#uploadfile").attr("action", "/addBatchTeacher/")
                } else if (type == 3) {
                    $("#uploadfile").attr("action", "/addBatchAdmin/")
                }
            })
        });
        $(".adduserdown").each(function () {
            $(this).unbind('click').bind('click', function () {
                type = $("#type").attr('attr')
                if (type == "") {
                    alert("请选择要添加的用户身份！")
                }
                window.open("/getlisttemplate/?type=" + type);
            })
        });
        //确认取消
        $(".addusersure").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".addusercancle").bind("click", function () {
            alert($(this).text())
        })
    },
    //学生端未完成的实验
    indexEvent: function () {
        var me = this;
        //预览实验
        $(".preview").each(function () {
            $(this).unbind('click').bind('click', function () {
                videostr = $(this).attr("videos")
                $('.popupbox').show()
                $('.popupwall9').show()
                videos = JSON.parse(videostr)
                videohtml = ""
                for (index in videos) {
                    videohtml = videohtml + '<div vaddress="' + videos[index].url + '" class=\"vchange\" videoname=\"' + videos[index].name + '\"><div class=\"v_svideo\"><img src="../static/img/videologo.png" alt=""></div><div class=\"v_svideoname\">' + videos[index].name + '</div></div>';
                    if (index == 0) {
                        if (index == 0) {
                            var videoStr = ' <div class="videobox">\n' +
                                '                <video id="video" style="width:100%;height:auto" controls>\n' +
                                '                    <source src="' + videos[index].url + '" type="video/mp4">\n' +
                                '                </video>\n' +
                                '            </div>'
                            $(".vbox").html(videoStr)
                            $("#videoname").html(videos[index].name)
                        }
                    }
                }
                $(".vchangebox").html(videohtml)
                $(".vchange").each(function () {
                    $(this).unbind('click').bind('click', function () {
                        url = $(this).attr("vaddress")
                        videoname = $(this).attr("videoname")
                        var videoStr = ' <div class="videobox">\n' +
                            '                <video id="video" style="width:100%;height:auto" controls>\n' +
                            '                    <source src="' + url + '" type="video/mp4">\n' +
                            '                </video>\n' +
                            '            </div>'
                        $(".vbox").html(videoStr)
                        $("#videoname").html(videoname)
                        me.hidePopup()
                    })
                })
            })
        });
        //实验数据下载
        $(".datadownload").each(function () {
            $(this).unbind('click').bind('click', function () {
                dataurl = $(this).attr("dataurl")
                if (dataurl == "") {
                    alert("文件不存在")
                }
                window.open("/downloaddata/?dataurl=" + dataurl);
            })
        });
        //虚拟实验操作
        $(".operation").each(function () {
            $(this).unbind('click').bind('click', function () {
                experimentid = $(this).attr("experimentid")
                window.location.href = experimentid
            })
        });
        //提交实验报告
        $(".submit").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall6').show()
                reportid = $(this).attr("reportid")
                $(".reportid").attr("value", reportid)
            })
        });
        //报告模板下载
        $(".templatedownload").each(function () {
            $(this).unbind('click').bind('click', function () {
                templateid = $(this).attr("templateid")
                window.open("/downloadtemplate/?templateid=" + templateid);
            })
        });
        //上传文件
        $(".uploadfile").bind('click', function (e) {
            me.fileUpLoad(e)
        })
        //确认取消
        $(".indexcancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".indexsure").bind("click", function () {
            alert($(this).text())
        })
    },
    //学生全部实验
    allexpEvent: function () {
        $(".allpreview").each(function () {
            $(this).unbind('click').bind('click', function () {
                videostr = $(this).attr("videos")
                $('.popupbox').show()
                $('.popupwall9').show()
                videos = JSON.parse(videostr)
                videohtml = ""
                for (index in videos) {
                    videohtml = videohtml + '<div vaddress="' + videos[index].url + '" class=\"vchange\" videoname=\"' + videos[index].name + '\"><div class=\"v_svideo\"><img src="../static/img/videologo.png" alt=""></div><div class=\"v_svideoname\">' + videos[index].name + '</div></div>';
                    if (index == 0) {
                        if (index == 0) {
                            var videoStr = ' <div class="videobox">\n' +
                                '                <video id="video" style="width:100%;height:auto" controls>\n' +
                                '                    <source src="' + videos[index].url + '" type="video/mp4">\n' +
                                '                </video>\n' +
                                '            </div>'
                            $(".vbox").html(videoStr)
                            $("#videoname").html(videos[index].name)
                        }
                    }
                }
                $(".vchangebox").html(videohtml)
                $(".vchange").each(function () {
                    $(this).unbind('click').bind('click', function () {
                        url = $(this).attr("vaddress")
                        videoname = $(this).attr("videoname")
                        var videoStr = ' <div class="videobox">\n' +
                            '                <video id="video" style="width:100%;height:auto" controls>\n' +
                            '                    <source src="' + url + '" type="video/mp4">\n' +
                            '                </video>\n' +
                            '            </div>'
                        $(".vbox").html(videoStr)
                        $("#videoname").html(videoname)
                        me.hidePopup()
                    })
                })
            })
        });

        $(".alloperation").each(function () {
            $(this).unbind('click').bind('click', function () {
                experimentid = $(this).attr("experimentid")
                window.location.href = experimentid
            })
        });

        $(".alldownload").each(function () {
            $(this).unbind('click').bind('click', function () {
                templateid = $(this).attr("templateid")
                window.open("/downloadtemplate/?templateid=" + templateid);
            })
        });

        $(".allcancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".allsure").bind("click", function () {
            alert($(this).text())
        })
    },
    //学生用户列表管理
    studentmanagementEvent: function () {
        $(".deleuser").each(function () {
            $(this).unbind('click').bind('click', function () {
                if (confirm("删除学生用户后不可恢复，是否要执行此操作？")) {
                    studentid = $(this).attr("studentid")
                    $.post("/deleteStudentByid/",
                        {
                            studentid: studentid
                        },
                        function (data, status) {
                            dataObj = $.parseJSON(data)
                            code = dataObj.code;
                            if (code == -2) {//未登录
                                window.location = "/loginadmin/";
                            } else if (code != 0) {
                                alert(dataObj.desc);
                            } else {
                                alert("删除成功！")
                                window.location.reload()
                            }
                        });
                }
            })
        });
        $(".smcancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".smsure").bind("click", function () {
            alert($(this).text())
        })
    },
    //老师用户列表管理
    teachermanagementEvent: function () {
        $(".deletea").each(function () {
            $(this).unbind('click').bind('click', function () {
                if (confirm("删除教师用户后不可恢复，是否要执行此操作？")) {
                    teacherid = $(this).attr("teacherid")
                    $.post("/deleteTeacherByid/",
                        {
                            teacherid: teacherid
                        },
                        function (data, status) {
                            dataObj = $.parseJSON(data)
                            code = dataObj.code;
                            if (code == -2) {//未登录
                                window.location = "/loginadmin/";
                            } else if (code != 0) {
                                alert(dataObj.desc);
                            } else {
                                window.location.reload()
                            }
                        });
                }
            })
        });
        $(".tmcancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".tmsure").bind("click", function () {
            alert($(this).text())
        })
        $(".tsearch").bind('click', function () {
            searchname = $(".searchname").val();
            searchnum = $(".searchnum").val();
            var param = "?";
            if (searchname != "") {
                param = param + "searchname=" + searchname
            }
            if (searchnum != "") {
                if (param != "?") {
                    param = param + "&"
                }
                param = param + "searchnum=" + searchnum
            }

            if (param == "?") {
                param = "";
            }
            $(location).attr('href', '/teachermanagement/' + param);
        })
    },
    //管理员用户列表
    adminmanagementEvent: function () {
        $(".deleadmin").each(function () {
            $(this).unbind('click').bind('click', function () {
                if (confirm("删除管理员用户后不可恢复，是否要执行此操作？")) {
                    adminid = $(this).attr("adminid")
                    $.post("/deleteAdminByid/",
                        {
                            adminid: adminid
                        },
                        function (data, status) {
                            dataObj = $.parseJSON(data)
                            code = dataObj.code;
                            if (code == -2) {//未登录
                                window.location = "/loginadmin/";
                            } else if (code != 0) {
                                alert(dataObj.desc);
                            } else {
                                window.location.reload()
                            }
                        });
                }
            })
        });
        $(".amcancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".amsure").bind("click", function () {
            alert($(this).text())
        })
    },
    //进行中的教学
    undoneteachingEvent: function () {
        var me = this;
        $(".videobox").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.videobox').removeClass('selectvideobox')
                $(this).addClass('selectvideobox')
                me.videoDom = $(this)
            })
        });
        $('.changvideo2').unbind('click').bind('click', function () {
            me.addvideotype = "1"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $(".preadd2").unbind('click').bind('click', function () {
            me.addvideotype = "2"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $(".behindadd2").unbind('click').bind('click', function () {
            me.addvideotype = "3"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $('.cvdele2').unbind('click').bind('click', function () {
            if (me.videoDom != undefined) {
                if (confirm("确认要删除此视频么？")) {
                    me.videoDom.remove()
                    me.videoDom = undefined
                }
            } else {
                alert('请先选中一个视频！')
            }
        })
        $(".uteaupload").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall2').show()
                $(".popupmid").hide()
                $(".popupmid1").show()
                teachingid = $(this).attr("teachingid")
                $("#teachingid").attr("value", teachingid)
                $("#uploadfile").attr("action", "/uploadData/")
            })
        });
        $(".teastulist").each(function () {
            $(this).unbind('click').bind('click', function () {
                stulisturl = $(this).attr("stulisturl")
                if (stulisturl == "") {
                    alert("文件不存在")
                }
                window.open("/downloadStudentList/?stulisturl=" + stulisturl);
            })
        });
        $(".updatamod").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall2').show()
                $(".popupmid").hide()
                $(".popupmid2").show()
                teachingid = $(this).attr("teachingid")
                experimentid = $(this).attr("experimentid")
                $("#teachingid").attr("value", teachingid)
                $("#experimentid").attr("value", experimentid)
                $("#uploadfile").attr("action", "/updateTeachingTemplate/")
            })
        });
        $(".changevide2").each(function () {
            $(this).unbind('click').bind('click', function () {
                $("#videoexperimentid").val($(this).attr("experimentid"))
                $("#changevideoteachingid").val($(this).attr("teachingid"))
                var videostr = $(this).attr("videos");
                $(".videowall").html("")
                var videos = JSON.parse(videostr)
                for (var i = 0, len = videos.length; i < len; i++) {
                    var domStr = ' <div class="videobox" videoid = "' + videos[i].id + '">\n' +
                        '                   ' + videos[i].name + '\n' +
                        '                </div>'
                    $(".videowall").append(domStr)
                }
                $(".videobox").each(function () {
                    $(this).unbind('click').bind('click', function () {
                        $('.videobox').removeClass('selectvideobox')
                        $(this).addClass('selectvideobox')
                        me.videoDom = $(this)
                    })
                });

                $('.popupbox').show()
                $('.popupwall5').show()

            })
        });
        $(".changedata").each(function () {
            $(this).unbind('click').bind('click', function () {
                alert()
                $('.popupbox').show()
                $('.popupwall4').show()
                $("#zane-calendar").html($(this).attr("deadline"))
                $("#udpatedeadlineid").val($(this).attr("teachingid"))
            })
        });
        $(".uteadele").each(function () {
            $(this).unbind('click').bind('click', function () {
                if (confirm("实验教学删除不可恢复，确认要删除吗？")) {
                    teachingid = $(this).attr("teachingid")
                    $.post("/deleteTeachingByid/",
                        {
                            teachingid: teachingid
                        },
                        function (data, status) {
                            dataObj = $.parseJSON(data)
                            code = dataObj.code;
                            if (code == -2) {//未登录
                                window.location = "/loginteacher/";
                            } else if (code != 0) {
                                alert(dataObj.desc);
                            } else {
                                window.location.reload()
                            }
                        });
                }
            })
        });

        $(".downloadscore").each(function () {
            $(this).unbind('click').bind('click', function () {
                teachingid = $(this).attr("teachingid")
                if (teachingid == "") {
                    alert("请刷新网页后重试！")
                }
                window.open("/downloadReportScoreList/?teachingid=" + teachingid);
            })
        });
        $(".upexpdata").each(function () {
            $(this).unbind('click').bind('click', function () {
                $(".popupmid").hide()
                $('.popupbox').show()
                $('.popupwall2').show()
                $('.popupmid1').show()
            })
        });
        $(".uteasure").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".uteacancle").bind("click", function () {
        })
        $(".updatedeadlinesure").bind("click", function () {
            datehtml = $("#zane-calendar").html()
            if (datehtml == "") {
                alert("请选择日期！")
                return;
            }
            re = new RegExp("/", "g")
            datestr = datehtml.replace(re, "-")
            teachingid = $("#udpatedeadlineid").val()
            $.post("/updateTeachingDeadline/",
                {
                    teachingid: teachingid,
                    deadline: datestr
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code == -2) {//未登录
                        window.location = "/loginteacher/";
                    } else if (code != 0) {
                        alert(dataObj.desc);
                    } else {
                        alert("更改成功！")
                        window.location.reload()
                    }
                });

        })
        $(".updatedeadlinecancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".changvideosure2").unbind('click').bind("click", function () {
            $("#addvideotype").val(1)
            var options = {
                url: "/uploadVideo/", //提交地址：默认是form的action,如果申明,则会覆盖
                type: "post",   //默认是form的method（get or post），如果申明，则会覆盖
                beforeSubmit: beforeCheck, //提交前的回调函数
                success: successChangeVideo,  //提交成功后的回调函数
                target: "#addvideo",  //把服务器返回的内容放入id为output的元素中
                dataType: "json", //html(默认), xml, script, json...接受服务端返回的类型
                clearForm: false,  //成功提交后，是否清除所有表单元素的值
                resetForm: false,  //成功提交后，是否重置所有表单元素的值
                timeout: 3000     //限制请求的时间，当请求大于3秒后，跳出请求
            };
            console.log(me.addepxupdatamodObj)
            console.log(me.addexpteastulistObj)
            console.log(me.addexpupexpdataObj)
            console.log(me.videodataObj)
            console.log(me.dataObjKind)
            $("#addvideo").ajaxSubmit(options)

            function successChangeVideo(data, status) {
                if ("success" != status) {
                    alert("网络异常，请重试！")
                }
                dataObj = data
                code = dataObj.code;
                if (code == -2) {//未登录
                    window.location = "/loginteacher/";
                } else if (code != 0) {
                    alert(dataObj.desc);
                    return;
                }
                var addvideotype = $("#addvideotype").attr("value")
                if (me.addvideotype == "1") {
                    if (me.videoDom != undefined) {
                        result = JSON.parse(dataObj.res);
                        me.videoDom.attr("videoid", result.id)
                        me.videoDom.html(result.name)
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else if (me.addvideotype == "2") {
                    result = JSON.parse(dataObj.res);
                    var domStr = ' <div class="videobox" videoid="' + result.id + '">\n' +
                        '                   ' + result.name + '\n' +
                        '                </div>'
                    if (me.videoDom != undefined) {
                        me.videoDom.before(domStr)
                        me.videoDom = undefined
                        me.changePreVideo()
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else if (me.addvideotype == "3") {
                    result = JSON.parse(dataObj.res);
                    var domStr = ' <div class="videobox" videoid="' + result.id + '">\n' +
                        '                   ' + result.name + '\n' +
                        '                </div>'
                    if (me.videoDom != undefined) {
                        me.videoDom.after(domStr)
                        me.videoDom = undefined
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else {
                    alert("网络异常，请重试！")
                }
                me.addvideotype = "0"
                $(".videofileuploadname").html('')
                $(".shuomingbox").val('')
                $('.videobox').removeClass('selectvideobox')
            }
        });
        $(".vbover2").unbind('click').bind("click", function () {
            videoitemlist = $(".videowall").children()
            var teachingid = $("#changevideoteachingid").val()
            var videoids = ""
            for (var i = 0; i < videoitemlist.length; i++) {
                if (i == 0) {
                    videoids = videoids + videoitemlist[i].getAttribute("videoid")
                } else {
                    videoids = videoids + "," + videoitemlist[i].getAttribute("videoid")
                }
            }
            $.post("/updateTeachingVideo/",
                {
                    teachingid: teachingid,
                    videos: videoids
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code == -2) {//未登录
                        window.location = "/loginteacher/";
                    } else if (code != 0) {
                        alert(dataObj.desc);
                        $('.popupbox').hide()
                        $('.popupwall5').hide()
                    } else {
                        $('.popupbox').hide()
                        $('.popupwall5').hide()
                        window.location.reload()
                    }
                });
        })
    },
    //已完成教学
    completedteachingEvent: function () {
        $(".uteadownload").each(function () {
            $(this).unbind('click').bind('click', function () {
                dataurl = $(this).attr("dataurl")
                if (dataurl == "") {
                    alert("文件不存在")
                }
                window.open("/downloaddata/?dataurl=" + dataurl);
            })
        });
        $(".teastulist").each(function () {
            $(this).unbind('click').bind('click', function () {
                stulisturl = $(this).attr("stulisturl")
                if (stulisturl == "") {
                    alert("文件不存在")
                }
                window.open("/downloadStudentList/?stulisturl=" + stulisturl);
            })
        });
        $(".downloaddatamod").each(function () {
            $(this).unbind('click').bind('click', function () {
                templateid = $(this).attr("templateid")
                window.open("/downloadtemplate/?templateid=" + templateid);
            })
        });
        //预览实验
        $(".preview").each(function () {
            $(this).unbind('click').bind('click', function () {
                videostr = $(this).attr("videos")
                $('.popupbox').show()
                $('.popupwall9').show()
                videos = JSON.parse(videostr)
                videohtml = ""
                for (index in videos) {
                    videohtml = videohtml + '<div vaddress="' + videos[index].url + '" class=\"vchange\" videoname=\"' + videos[index].name + '\"><div class=\"v_svideo\"><img src="../static/img/videologo.png" alt=""></div><div class=\"v_svideoname\">' + videos[index].name + '</div></div>';
                    if (index == 0) {
                        if (index == 0) {
                            var videoStr = ' <div class="videobox">\n' +
                                '                <video id="video" style="width:100%;height:auto" controls>\n' +
                                '                    <source src="' + videos[index].url + '" type="video/mp4">\n' +
                                '                </video>\n' +
                                '            </div>'
                            $(".vbox").html(videoStr)
                            $("#videoname").html(videos[index].name)
                        }
                    }
                }
                $(".vchangebox").html(videohtml)
                $(".vchange").each(function () {
                    $(this).unbind('click').bind('click', function () {
                        url = $(this).attr("vaddress")
                        videoname = $(this).attr("videoname")
                        var videoStr = ' <div class="videobox">\n' +
                            '                <video id="video" style="width:100%;height:auto" controls>\n' +
                            '                    <source src="' + url + '" type="video/mp4">\n' +
                            '                </video>\n' +
                            '            </div>'
                        $(".vbox").html(videoStr)
                        $("#videoname").html(videoname)
                        me.hidePopup()
                    })
                })
            })
        });
        $(".changedata").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall4').show()
                $("#zane-calendar").html($(this).attr("deadline"))
                $("#udpatedeadlineid").val($(this).attr("teachingid"))
            })
        });
        $(".uteasure").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".uteacancle").bind("click", function () {
            datehtml = $("#zane-calendar").html()
            if (datehtml == "") {
                alert("请选择日期！")
                return;
            }
            re = new RegExp("/", "g")
            datestr = datehtml.replace(re, "-")
            teachingid = $("#udpatedeadlineid").val()
            $.post("/updateTeachingDeadline/",
                {
                    teachingid: teachingid,
                    deadline: datestr
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code == -2) {//未登录
                        window.location = "/loginteacher/";
                    } else if (code != 0) {
                        alert(dataObj.desc);
                    } else {
                        alert("更改成功！")
                        window.location.reload()
                    }
                });
        })
    },
    //全部实验教师端
    allexpteaEvent: function () {
        var me = this;
        $(".videobox").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.videobox').removeClass('selectvideobox')
                $(this).addClass('selectvideobox')
                me.videoDom = $(this)
            })
        });
        $('.changvideo2').unbind('click').bind('click', function () {
            me.addvideotype = "1"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $(".preadd2").unbind('click').bind('click', function () {
            me.addvideotype = "2"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $(".behindadd2").unbind('click').bind('click', function () {
            me.addvideotype = "3"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $('.cvdele2').unbind('click').bind('click', function () {
            if (me.videoDom != undefined) {
                if (confirm("确认要删除此视频么？")) {
                    me.videoDom.remove()
                    me.videoDom = undefined
                }
            } else {
                alert('请先选中一个视频！')
            }
        })
        $(".allteapreview").each(function () {
            $(this).unbind('click').bind('click', function () {
                videostr = $(this).attr("videos")
                $('.popupbox').show()
                $('.popupwall9').show()
                videos = JSON.parse(videostr)
                videohtml = ""
                for (index in videos) {
                    videohtml = videohtml + '<div vaddress="' + videos[index].url + '" class=\"vchange\" videoname=\"' + videos[index].name + '\"><div class=\"v_svideo\"><img src="../static/img/videologo.png" alt=""></div><div class=\"v_svideoname\">' + videos[index].name + '</div></div>';
                    if (index == 0) {
                        if (index == 0) {
                            var videoStr = ' <div class="videobox">\n' +
                                '                <video id="video" style="width:100%;height:auto" controls>\n' +
                                '                    <source src="' + videos[index].url + '" type="video/mp4">\n' +
                                '                </video>\n' +
                                '            </div>'
                            $(".vbox").html(videoStr)
                            $("#videoname").html(videos[index].name)
                        }
                    }
                }
                $(".vchangebox").html(videohtml)
                $(".vchange").each(function () {
                    $(this).unbind('click').bind('click', function () {
                        url = $(this).attr("vaddress")
                        videoname = $(this).attr("videoname")
                        var videoStr = ' <div class="videobox">\n' +
                            '                <video id="video" style="width:100%;height:auto" controls>\n' +
                            '                    <source src="' + url + '" type="video/mp4">\n' +
                            '                </video>\n' +
                            '            </div>'
                        $(".vbox").html(videoStr)
                        $("#videoname").html(videoname)
                        me.hidePopup()
                    })
                })
            })
        });
        $(".changvideosure2").unbind('click').bind("click", function () {
            $("#addvideotype").val(1)
            var options = {
                url: "/uploadVideo/", //提交地址：默认是form的action,如果申明,则会覆盖
                type: "post",   //默认是form的method（get or post），如果申明，则会覆盖
                beforeSubmit: beforeCheck, //提交前的回调函数
                success: successChangeVideo,  //提交成功后的回调函数
                target: "#addvideo",  //把服务器返回的内容放入id为output的元素中
                dataType: "json", //html(默认), xml, script, json...接受服务端返回的类型
                clearForm: false,  //成功提交后，是否清除所有表单元素的值
                resetForm: false,  //成功提交后，是否重置所有表单元素的值
                timeout: 3000     //限制请求的时间，当请求大于3秒后，跳出请求
            };
            console.log(me.addepxupdatamodObj)
            console.log(me.addexpteastulistObj)
            console.log(me.addexpupexpdataObj)
            console.log(me.videodataObj)
            console.log(me.dataObjKind)
            $("#addvideo").ajaxSubmit(options)

            function successChangeVideo(data, status) {
                if ("success" != status) {
                    alert("网络异常，请重试！")
                }
                dataObj = data
                code = dataObj.code;
                if (code == -2) {//未登录
                    window.location = "/loginteacher/";
                } else if (code != 0) {
                    alert(dataObj.desc);
                    return;
                }
                var addvideotype = $("#addvideotype").attr("value")
                if (me.addvideotype == "1") {
                    if (me.videoDom != undefined) {
                        result = JSON.parse(dataObj.res);
                        me.videoDom.attr("videoid", result.id)
                        me.videoDom.html(result.name)
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else if (me.addvideotype == "2") {
                    result = JSON.parse(dataObj.res);
                    var domStr = ' <div class="videobox" videoid="' + result.id + '">\n' +
                        '                   ' + result.name + '\n' +
                        '                </div>'
                    if (me.videoDom != undefined) {
                        me.videoDom.before(domStr)
                        me.videoDom = undefined
                        me.changePreVideo()
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else if (me.addvideotype == "3") {
                    result = JSON.parse(dataObj.res);
                    var domStr = ' <div class="videobox" videoid="' + result.id + '">\n' +
                        '                   ' + result.name + '\n' +
                        '                </div>'
                    if (me.videoDom != undefined) {
                        me.videoDom.after(domStr)
                        me.videoDom = undefined
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else {
                    alert("网络异常，请重试！")
                }
                me.addvideotype = "0"
                $(".videofileuploadname").html('')
                $(".shuomingbox").val('')
                $('.videobox').removeClass('selectvideobox')
            }
        });
        $(".allteaoperation").each(function () {
            $(this).unbind('click').bind('click', function () {
                window.location.href = $(this).attr("experimenturl")
            })
        });
        $(".downloaddatamod").each(function () {
            $(this).unbind('click').bind('click', function () {
                templateid = $(this).attr("templateid")
                window.open("/downloadtemplate/?templateid=" + templateid);
            })
        });
        $(".allteacancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".allteasure").bind("click", function () {
            alert($(this).text())
        })
        $(".changevide2").each(function () {
            $(this).unbind('click').bind('click', function () {
                $("#videoexperimentid").val($(this).attr("experimentid"))
                $("#changevideoexperimentid").val($(this).attr("experimentid"))
                var videostr = $(this).attr("videos");
                $(".videowall").html("")
                var videos = JSON.parse(videostr)
                for (var i = 0, len = videos.length; i < len; i++) {
                    var domStr = ' <div class="videobox" videoid = "' + videos[i].id + '">\n' +
                        '                   ' + videos[i].name + '\n' +
                        '                </div>'
                    $(".videowall").append(domStr)
                }
                $(".videobox").each(function () {
                    $(this).unbind('click').bind('click', function () {
                        $('.videobox').removeClass('selectvideobox')
                        $(this).addClass('selectvideobox')
                        me.videoDom = $(this)
                    })
                });

                $('.popupbox').show()
                $('.popupwall5').show()

            })
        });
        //修改实验描述
        $(".changedescription").each(function () {
            $(this).unbind('click').bind('click', function () {
                // $("#videoexperimentid").val($(this).attr("experimentid"))
                $("#des_title").val("修改 "+$(this).attr("experimentname")+" 的实验描述")
                $("#des_content").val($(this).attr("experimentdesc"))
                $("#des_id").val($(this).attr("experimentid"))


                // var videostr = $(this).attr("videos");
                // $(".videowall").html("")
                // var videos = JSON.parse(videostr)
                // for (var i = 0, len = videos.length; i < len; i++) {
                //     var domStr = ' <div class="videobox" videoid = "' + videos[i].id + '">\n' +
                //         '                   ' + videos[i].name + '\n' +
                //         '                </div>'
                //     $(".videowall").append(domStr)
                // }
                // $(".videobox").each(function () {
                //     $(this).unbind('click').bind('click', function () {
                //         $('.videobox').removeClass('selectvideobox')
                //         $(this).addClass('selectvideobox')
                //         me.videoDom = $(this)
                //     })
                // });

                $('.setdescription').show()
                $('.popupbox').show()
                $('.popupwall5').show()

            })
        });
        $(".vbover3").unbind('click').bind("click", function () {
            videoitemlist = $(".videowall").children()
            var experimentid = $("#changevideoexperimentid").val()
            var videoids = ""
            for (var i = 0; i < videoitemlist.length; i++) {
                if (i == 0) {
                    videoids = videoids + videoitemlist[i].getAttribute("videoid")
                } else {
                    videoids = videoids + "," + videoitemlist[i].getAttribute("videoid")
                }
            }
            $.post("/updateExperimentVideo/",
                {
                    experimentid: experimentid,
                    videos: videoids
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code == -2) {//未登录
                        window.location = "/loginteacher/";
                    } else if (code != 0) {
                        alert(dataObj.desc);
                        $('.popupbox').hide()
                        $('.popupwall5').hide()
                    } else {
                        $('.popupbox').hide()
                        $('.popupwall5').hide()
                        window.location.reload()
                    }
                });
        })
        $(".updatamod").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall2').show()
                $(".popupmid").hide()
                $(".popupmid2").show()
                experimentid = $(this).attr("experimentid")
                $("#experimentid").attr("value", experimentid)
                $("#uploadfile").attr("action", "/updateExperimentTemplate/")
            })
        });
    },
    //审批
    approvalEvent: function () {
        $(".approval").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.popupbox').show()
                $('.popupwall1').show()
                stuname = $('.t_txt2').html()
                stunumber = $('.t_txt3').html()
                reportid = $(this).attr("reportid")
                reporturl = $(this).attr("reporturl")
                $("#pstudentname").text("姓名：" + stuname)
                $("#pstudentid").text("学号：" + stunumber)
                $("#preportid").attr("value", reportid)
                var domain = document.domain;
                var port = location.port;
                // var reporturl = "http://" + domain + ":" + port + "/downloadReport/?reproturl=" + reporturl
                // $("#reportifreameid").attr("src", "/downloadReport/?reproturl=" + reporturl)
                $("#reportalinkid").href("/downloadReport/?reproturl=" + reporturl)

            })
        });
        $(".approvalcancle").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".approvalsure").bind("click", function () {
            var reportid = $("#preportid").attr("value")
            var score = $("#pscore").val()
            if (reportid == undefined || reportid == "") {
                if (confirm("选择批阅的报告错误，请重新选择")) {
                    $('.popupbox').hide()
                    $('.popupwall').hide()
                } else {
                    $('.popupbox').hide()
                    $('.popupwall').hide()
                }
                return
            }
            if (score == "0" || score == "" || score > 100) {
                alert("打分异常")
                return
            }
            $.post("/scoreReport/",
                {
                    reportid: reportid,
                    score: score
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code == -2) {//未登录
                        window.location = "/loginteacher/";
                    } else if (code != 0) {
                        alert(dataObj.desc);
                    } else {
                        window.location.reload()
                    }
                });
        })
    },
    //修改密码
    changePossword: function () {
        $(".pwcancel").bind('click', function () {
            javascript:history.back(-1);
        });
        $(".pwsure").bind('click', function () {
            var oldpwd = $(".oldpwd").val();
            var newpwd = $(".newpwd").val();
            var newpwd2 = $(".newpwd2").val();
            if (newpwd != newpwd2) {
                alert("两次输入的密码不一致!");
            }
            $.post("/passwordedit/",
                {
                    oldpwd: sha256_digest(oldpwd),
                    newpwd: sha256_digest(newpwd)
                },
                function (data, status) {
                    dataObj = $.parseJSON(data)
                    code = dataObj.code;
                    if (code == -2) {//未登录
                        window.location = "/loginteacher/";
                    } else if (code != 0) {
                        alert(dataObj.desc);
                    } else {
                        alert("修改成功")
                        $.cookie("teacherid", "", {expires: -1});
                        $.cookie("teachernumber", "", {expires: -1});
                        $.cookie("teachername", "", {expires: -1});
                        location.href = '/loginteacher/'
                    }
                });

        })
    },
    // 关闭弹窗
    hidePopup: function () {
        var me = this
        $('.dele').bind('click', function () {
            $('.setdescription').hide()
            $('.addstudent').hide()
            $('.popupbox').hide()
            $('.popupwall').hide()
            $('.fileuploadname').html('')
            me.dataObjKind = 0;
            try {
                video.pause()
            } catch (e) {

            }
            $(".vbox").html("")
        })
    },
    //选择文件
    fileUpLoad: function () {
        var file = event.target.files[0];
        $(".fileuploadname").html(file.name)
        var e = window.event || event;
        //传递给后台的formdata对象
        var data = new FormData();
        data.append("filesData", file);
        //传递给后台的obj对象
        this.fileDataObj = data;
    },
    //上传模板文件
    addepxupdatamodFileup: function () {
        var file = event.target.files[0];
        $(".addepxupdatamodFileupname").html(file.name)
    },
    //上传实验数据
    updataradioFileup: function () {
        var file = event.target.files[0];
        $(".updataradioname").html(file.name)
    },
    //上传学生名单
    upstulistFileup: function () {
        var file = event.target.files[0];
        $(".upstulistname").html(file.name)
    },
    //上传修改视频
    updataChangeVideo: function () {
        var file = event.target.files[0];
        $(".videofileuploadname").html(file.name)
    },
    //上传文件
    upLoad: function () {
        var me = this;
        $(".fileupload").bind('click', function () {
            var data = me.fileDataObj;
            console.log(data)
            $.post("约定地址", data, function (result) {
                console.log(result);
            })
        })

    },
    //更改播放视频
    changeVideo: function (e) {
        var me = this
        var vAddress = $('this').attr("class")
        $(".vchange").each(function () {
            $(this).unbind('click').bind('click', function () {
                url = $(this).attr("vaddress")
                videoname = $(this).attr("videoname")
                $("#video").parentNode.removeChild($("#video"));
                sourceDom = $("<source id=\"videosource\" src=\"" + url + "\">");
                $("#video").append(sourceDom);
                $("#videoname").html(videoname)
                //me.hidePopup()
            })
        });
    },
    //时间选择插件
    calendar: function () {
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        var nowTime = year + '-' + month + '-' + day
        zaneDate({
            elem: '#zane-calendar',
            showtime: false,
            begintime: nowTime,
            behindTop: -40,
            haveBotBtns: false,
        })
    },
    //新增实验
    radioBtn: function () {
        var me = this
        //上传模板文件
        $(".addepxupdatamod").each(function () {
            $(this).unbind('click').bind('click', function () {
                me.dataObjKind = 1

            })
        });
        //上传学生名单
        $(".addexpteastulist").each(function () {
            $(this).unbind('click').bind('click', function () {
                me.dataObjKind = 2


            })
        });
        //上传实验数据
        $(".addexpupexpdata").each(function () {
            $(this).unbind('click').bind('click', function () {
                me.dataObjKind = 3

            })
        });
        //修改视屏
        $('.v_dele').each(function (index, domEle) {
            $(this).unbind('click').bind('click', function () {
                alert($(this).text())
            })
        });
        $('.v_change').each(function (index, domEle) {
            $(this).unbind('click').bind('click', function () {
                me.dataObjKind = 4

            })
        });
        $(".addexpcancle").unbind('click').bind("click", function () {
            datehtml = $("#zane-calendar").html()
            if (datehtml == "") {
                alert("请选择日期！")
                return;
            }
            re = new RegExp("/", "g")
            datestr = datehtml.replace(re, "-")
            $("#addcalendarhtml").html(datehtml)
            $("#addcalendar").val(datestr)

            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".addexuteasure").bind("click", function () {
            $('.popupbox').hide()
            $('.popupwall').hide()
        })
        $(".addexpstudentdown").unbind('click').bind("click", function () {
            window.open("/getlisttemplate/?type=1");
        })
        $(".addcalendar").unbind('click').bind("click", function () {
            $('.popupbox').show()
            $('.popupwall4').show()
        })
        $('.updataradio').each(function (index, domEle) {
            $(this).unbind('click').bind('click', function () {
                var val = $(this).val()
                if (val == 2) {
                    $(".addexpupexpdata").show()
                } else {
                    $(".addexpupexpdata").hide()
                    $(".updataradioname").hide()
                    $(".updataradioname").html()
                }
            })
        });
        $('.uptemplate').each(function (index, domEle) {
            $(this).unbind('click').bind('click', function () {
                var val = $(this).val()
                if (val == 2) {
                    $(".addepxupdatamod").show()
                } else {
                    $(".addepxupdatamod").hide()
                    $(".addepxupdatamodFileupname").hide()
                    $(".addepxupdatamodFileupname").html()
                }
            })
        });

        //确认添加
        $(".addsurebtn").unbind('click').bind('click', function () {
            var options = {
                url: "/addexperiment/", //提交地址：默认是form的action,如果申明,则会覆盖
                type: "post",   //默认是form的method（get or post），如果申明，则会覆盖
                beforeSubmit: beforeCheck, //提交前的回调函数
                success: successfun,  //提交成功后的回调函数
                target: "#addexperiment",  //把服务器返回的内容放入id为output的元素中
                dataType: "json", //html(默认), xml, script, json...接受服务端返回的类型
                clearForm: false,  //成功提交后，是否清除所有表单元素的值
                resetForm: false,  //成功提交后，是否重置所有表单元素的值
                timeout: 3000,     //限制请求的时间，当请求大于3秒后，跳出请求
                async: false
            };
            console.log(me.addepxupdatamodObj)
            console.log(me.addexpteastulistObj)
            console.log(me.addexpupexpdataObj)
            console.log(me.videodataObj)
            console.log(me.dataObjKind)
            $("#addexperiment").ajaxSubmit(options)

            function successfun(data, status) {
                if ("success" != status) {
                    alert("网络异常，请重试！")
                }
                dataObj = data
                code = dataObj.code;
                if (code == -2) {//未登录
                    window.location = "/loginteacher/";
                } else if (code != 0) {
                    alert(dataObj.desc);
                }
                else {
                    alert("创建成功！")
                    window.location = "/addexp/"
                }
            }
        })
    },
    //修改预览视频
    changePreVideo: function () {
        var me = this;
        $(".videobox").each(function () {
            $(this).unbind('click').bind('click', function () {
                $('.videobox').removeClass('selectvideobox')
                $(this).addClass('selectvideobox')
                me.videoDom = $(this)
            })
        });
        $('.changvideo').unbind('click').bind('click', function () {
            me.addvideotype = "1"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $(".preadd").unbind('click').bind('click', function () {
            me.addvideotype = "2"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $(".behindadd").unbind('click').bind('click', function () {
            me.addvideotype = "3"
            if (me.videoDom != undefined) {
                $('.popupbox').show()
                $('.popupwall2_2').show()
            } else {
                alert('请先选择视频')
            }
        })
        $('.cvdele').unbind('click').bind('click', function () {
            if (me.videoDom != undefined) {
                if (confirm("确认要删除此视频么？")) {
                    me.videoDom.remove()
                    me.videoDom = undefined
                }
            } else {
                alert('请先选中一个视频！')
            }
        })
        $(".vbover").unbind('click').bind("click", function () {
            videoitemlist = $(".videowall").children()
            var videoids = ""
            for (var i = 0; i < videoitemlist.length; i++) {
                if (i == 0) {
                    videoids = videoids + videoitemlist[i].getAttribute("videoid")
                } else {
                    videoids = videoids + "," + videoitemlist[i].getAttribute("videoid")
                }
            }
            $("#videosinputid").attr("value", videoids);
            $('.popupbox').hide()
            $('.popupwall5').hide()
        })
        $(".changvideosure").unbind('click').bind("click", function () {
            $("#addvideotype").val(1)
            var options = {
                url: "/uploadVideo/", //提交地址：默认是form的action,如果申明,则会覆盖
                type: "post",   //默认是form的method（get or post），如果申明，则会覆盖
                beforeSubmit: beforeCheck, //提交前的回调函数
                success: successChangeVideo,  //提交成功后的回调函数
                target: "#addvideo",  //把服务器返回的内容放入id为output的元素中
                dataType: "json", //html(默认), xml, script, json...接受服务端返回的类型
                clearForm: false,  //成功提交后，是否清除所有表单元素的值
                resetForm: false,  //成功提交后，是否重置所有表单元素的值
                timeout: 3000     //限制请求的时间，当请求大于3秒后，跳出请求
            };
            console.log(me.addepxupdatamodObj)
            console.log(me.addexpteastulistObj)
            console.log(me.addexpupexpdataObj)
            console.log(me.videodataObj)
            console.log(me.dataObjKind)
            $("#addvideo").ajaxSubmit(options)

            function successChangeVideo(data, status) {
                if ("success" != status) {
                    alert("网络异常，请重试！")
                }
                dataObj = data
                code = dataObj.code;
                if (code == -2) {//未登录
                    window.location = "/loginteacher/";
                } else if (code != 0) {
                    alert(dataObj.desc);
                    return;
                }
                var addvideotype = $("#addvideotype").attr("value")
                if (me.addvideotype == "1") {
                    if (me.videoDom != undefined) {
                        result = JSON.parse(dataObj.res);
                        me.videoDom.attr("videoid", result.id)
                        me.videoDom.html(result.name)
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else if (me.addvideotype == "2") {
                    result = JSON.parse(dataObj.res);
                    var domStr = ' <div class="videobox" videoid="' + result.id + '">\n' +
                        '                   ' + result.name + '\n' +
                        '                </div>'
                    if (me.videoDom != undefined) {
                        me.videoDom.before(domStr)
                        me.videoDom = undefined
                        me.changePreVideo()
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else if (me.addvideotype == "3") {
                    result = JSON.parse(dataObj.res);
                    var domStr = ' <div class="videobox" videoid="' + result.id + '">\n' +
                        '                   ' + result.name + '\n' +
                        '                </div>'
                    if (me.videoDom != undefined) {
                        me.videoDom.after(domStr)
                        me.videoDom = undefined
                    } else {
                        alert('请先选中一个视频！')
                    }
                    me.changePreVideo()
                    $('.popupwall2_2').hide()
                } else {
                    alert("网络异常，请重试！")
                }
                me.addvideotype = "0"
                $(".videofileuploadname").html('')
                $(".shuomingbox").val('')
                $('.videobox').removeClass('selectvideobox')
            }
        })
        $(".changevdele,.changvideocancle").unbind('click').bind("click", function () {
            $(".popupwall2_2").hide()
            $(".videofileuploadname").html('')
            $(".shuomingbox").val('')
        })
        $(".changevide").each(function () {
            $(this).unbind('click').bind('click', function () {
                var experiment = $("#experimentid  option:selected")
                var videostr = experiment.attr("videos");
                if (videostr == undefined) {
                    alert("请选择实验！")
                    return
                }
                $('.popupbox').show()
                $('.popupwall5').show()
            })
        });

        //添加学生至实验学生名单
        $(".change_student_list").each(function () {
            $(this).unbind('click').bind('click', function () {
                var experiment = $("#experimentid  option:selected")
                var videostr = experiment.attr("videos");
                if (videostr == undefined) {
                    alert("请选择实验！")
                    return
                }
                $('.addstudent').show()
                $('.popupwall5').show()
            })
        });

        $("#experimentid").on('change', function () {
            var experiment = $("#experimentid  option:selected")
            $("#videoexperimentid").val(experiment.attr("value"))
            var videostr = experiment.attr("videos");
            $(".videowall").html("")
            var videos = JSON.parse(videostr)
            for (var i = 0, len = videos.length; i < len; i++) {
                var domStr = ' <div class="videobox" videoid = "' + videos[i].id + '">\n' +
                    '                   ' + videos[i].name + '\n' +
                    '                </div>'
                $(".videowall").append(domStr)
            }
            $(".videobox").each(function () {
                $(this).unbind('click').bind('click', function () {
                    $('.videobox').removeClass('selectvideobox')
                    $(this).addClass('selectvideobox')
                    me.videoDom = $(this)
                })
            });
            var videoids = $("#experimentid  option:selected").attr("videoids");
            $("#videosinputid").attr("value", videoids);
        })
    }

}
publicObj.init();