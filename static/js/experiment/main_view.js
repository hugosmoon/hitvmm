//可视化区域要显示的是切削力、温度、粗糙度？
var cut_cal_status;

//机床启动循环基数
var brc;
var brc_stop;
var count=0;
var count_stop=0;
//机床状态 1-加速 0-减速
var machine_status=1;


//基准角度
var basic_angle=0;
//基准角度变化率
var angle_change=0;

//时间戳
var shijianchuo;

//实际转速
var rot_speed_view=0;

//走刀距离
var knife_displacement=0;
//加工长度
var fabrication_length=0;

//角度和弧度的换算系数
var angle_xishu=0.0174533;

//画布高度
var height=400;
//夹盘中心盘半径
var center_wheel_r=120;
 //夹盘宽度
var d=20;

//背吃刀量
cutting_depth=0;

//主切削力
cutting_force=0;
cutting_temp=0;
cutting_r=0;

//_______________________________________________________________________________
//停止渲染
function stop_render(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius){
      machine_status=0;
      count_stop=0;
      shijianchuo=(new Date()).valueOf();

      if (brc) {
        clearTimeout(brc);
      }

    //重复调用渲染函数
      function render(){

        rendering(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius);

        if (rot_speed_view<0.001) {
            clearTimeout(brc_stop);
        }
        else {
            brc_stop=setTimeout(render,0);
        }
      }
      render();
}

//_______________________________________________________________________________
//开始渲染
function start_render(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius){
  machine_status=1;
  count=0;
  shijianchuo=(new Date()).valueOf();

  //重复调用渲染函数
  function render(){
    rendering(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius);
    brc=setTimeout(render,1);
  }
  render();

}

//_______________________________________________________________________________
//渲染函数
function rendering(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius){
  //获取每一帧的参数计算结果 实时转速 加工长度 基准角度
  var frame=frame_cal(feed_rate,rot_speed,workpiece_l);

  vertical_view(workpiece_r,workpiece_l,fabrication_length,cutting_depth);
  right_view(workpiece_r,workpiece_l,fabrication_length,cutting_depth);
  text_view(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius);
}

//_______________________________________________________________________________

  //计算每一帧的参数
function frame_cal(feed_rate,rot_speed,workpiece_l){

  new_shijianchuo=(new Date()).valueOf();
  // alert(new_shijianchuo);
  // alert(shijianchuo);
  if (new_shijianchuo != shijianchuo) {


    var jiasuxishu;
    if (machine_status==1) {
      //加速系数（模拟机床启动）
      jiasuxishu=(1-Math.pow((1/1.000001),Math.pow(2000*count/rot_speed,2.2)));
      //计算实时转速
      rot_speed_view=jiasuxishu*rot_speed;
      //基准角度变化量
      angle_change=jiasuxishu*(rot_speed/60)*((new_shijianchuo-shijianchuo)/1000)*360;
      //更新基准角度
      basic_angle+=angle_change;
    }
    if (machine_status==0) {
      //加速系数（模拟机床停止）
      jiasuxishu=1/Math.pow((count_stop+1),0.003);
      //计算实时转速
      rot_speed_view=rot_speed_view*jiasuxishu;
      count_stop+=1;
      //基准角度变化量
      angle_change=jiasuxishu*angle_change;
      //更新基准角度
      basic_angle+=angle_change;
    }




    //计算加工长度
      //刀尖走过的距离-全局变量  当机床开始减速的时候，刀尖停止运动
      if((rot_speed-rot_speed_view)<0.01&&(knife_displacement<=(workpiece_l-20))){
        knife_displacement+=(((new_shijianchuo-shijianchuo)/1000)*(rot_speed/60)*feed_rate);
      }
      //加工长度
      if(knife_displacement>=10&&(knife_displacement<=(workpiece_l+10))){
        fabrication_length=knife_displacement-+10
      }


    //更新时间戳
    shijianchuo=new_shijianchuo;
    //更新循环基数
    count+=1;

    return [rot_speed_view,fabrication_length,basic_angle]
  }
}

//_______________________________________________________________________________
//_______________________________________________________________________________
//_______________________________________________________________________________
//_______________________________________________________________________________

//渲染每一帧的图像
//_______________________________________________________________________________
//俯视图
function vertical_view(workpiece_r,workpiece_l,fabrication_length,cutting_depth){
  //清理画布
  $('#main_view').clearCanvas()
  $('#main_view').drawRect({
    fillStyle: 'rgb(20, 20, 30)',
    fromCenter:false,
    x: 0, y: 0,
    width: 1000,
    height: 500
  });
  //绘制网格

  for (var s = 0;s <1000;s=s+10) {
    $('#main_view').drawVector({
      strokeStyle: '#fff',
      strokeWidth: 0.1,
      x: 0, y: s,
      a1: 90, l1: 1000
    });
    $('#main_view').drawVector({
      strokeStyle: '#fff',
      strokeWidth: 0.1,
      x: s, y: 0,
      a1: 180, l1: 1000
    });
  }

  function xiebian(u,t){
    return Math.pow(( Math.pow(u,2) + Math.pow(t,2)),0.5);
  }

  //绘制夹盘-单层
  function sanjiajiabanhizhi(h1,center_wheel_r,jiapan_x,zxp_color,zxp_color_c,zxp_b){
    // 画中心盘
    $('#main_view').drawPath({
      fillStyle: $('canvas').createGradient({
        x1: 0, y1:  (height/2)-center_wheel_r,
        x2: 0, y2:  (height/2)+center_wheel_r,
        c1: zxp_color,
        c2: zxp_color_c, s2: 0.5,
        c3: zxp_color, s3: 1
      }),
      p1: {
        type: 'line',
        x1: jiapan_x, y1: (height/2)-center_wheel_r,
        x2: jiapan_x+zxp_b, y2: (height/2)-center_wheel_r,
        x3: jiapan_x+zxp_b, y3: (height/2)+center_wheel_r,
        x4: jiapan_x, y4: (height/2)+center_wheel_r,
        x5:jiapan_x,y5:(height/2)-center_wheel_r,
      },
    });

    //关键点位置坐标y
    pya1=Math.round((height/2)+xiebian((h1+center_wheel_r),(d/2))*Math.sin(-Math.atan(d/(2*(center_wheel_r+h1)))+basic_angle*angle_xishu));
    pyb1=Math.round((height/2)+xiebian((h1+center_wheel_r),(d/2))*Math.sin(Math.atan(d/(2*(center_wheel_r+h1)))+basic_angle*angle_xishu));
    pyc1=Math.round((height/2)+xiebian((center_wheel_r),(d/2))*Math.sin(-Math.atan(d/(2*(center_wheel_r)))+basic_angle*angle_xishu));
    pyd1=Math.round((height/2)+xiebian((center_wheel_r),(d/2))*Math.sin(Math.atan(d/(2*(center_wheel_r)))+basic_angle*angle_xishu));

    pya2=Math.round((height/2)+xiebian((h1+center_wheel_r),(d/2))*Math.sin(-Math.atan(d/(2*(center_wheel_r+h1)))+(basic_angle+120)*angle_xishu));
    pyb2=Math.round((height/2)+xiebian((h1+center_wheel_r),(d/2))*Math.sin(Math.atan(d/(2*(center_wheel_r+h1)))+(basic_angle+120)*angle_xishu));
    pyc2=Math.round((height/2)+xiebian((center_wheel_r),(d/2))*Math.sin(-Math.atan(d/(2*(center_wheel_r)))+(basic_angle+120)*angle_xishu));
    pyd2=Math.round((height/2)+xiebian((center_wheel_r),(d/2))*Math.sin(Math.atan(d/(2*(center_wheel_r)))+(basic_angle+120)*angle_xishu));

    pya3=Math.round((height/2)+xiebian((h1+center_wheel_r),(d/2))*Math.sin(-Math.atan(d/(2*(center_wheel_r+h1)))+(basic_angle+240)*angle_xishu));
    pyb3=Math.round((height/2)+xiebian((h1+center_wheel_r),(d/2))*Math.sin(Math.atan(d/(2*(center_wheel_r+h1)))+(basic_angle+240)*angle_xishu));
    pyc3=Math.round((height/2)+xiebian((center_wheel_r),(d/2))*Math.sin(-Math.atan(d/(2*(center_wheel_r)))+(basic_angle+240)*angle_xishu));
    pyd3=Math.round((height/2)+xiebian((center_wheel_r),(d/2))*Math.sin(Math.atan(d/(2*(center_wheel_r)))+(basic_angle+240)*angle_xishu));



    //绘制夹盘一个齿的函数
      function jiapanhuizhi(pya,pyb,pyc,pyd){
        if(pya<=pyb&&pya<=pyc&&pyc<=pyd){
          $('#main_view').drawPath({
            fillStyle: 'rgb(101, 105, 108)',
            p1:{
              type:'line',
              x1: jiapan_x+0, y1: pyb,
              x2: jiapan_x+0, y2: pya,
              x3: jiapan_x+zxp_b, y3: pya,
              x4: jiapan_x+zxp_b, y4: pyb,

            }
          });
          $('#main_view').drawPath({
            fillStyle: 'rgb(121, 125, 128)',
            p1:{
              type:'line',
              x1:jiapan_x+0,y1:pyb,
              x2:jiapan_x+0,y2:pyd,
              x3:jiapan_x+zxp_b,y3:pyd,
              x4:jiapan_x+zxp_b,y4:pyb,
            }
          });
        }
        if(pya>pyb&&pyb<=(height/2)-center_wheel_r){
          $('#main_view').drawPath({

            fillStyle: 'rgb(121, 125, 128)',
            p1:{
              type:'line',
              x1: jiapan_x+0, y1: (height/2)-center_wheel_r,
              x2: jiapan_x+0, y2: pyb,
              x3: jiapan_x+zxp_b, y3: pyb,
              x4: jiapan_x+zxp_b, y4:(height/2)-center_wheel_r,
              x5:jiapan_x+0,y5:(height/2)-center_wheel_r,
            }
          });
        }

        if(pya<=pyb&&pya>pyc&&pyc<=pyd){
          $('#main_view').drawPath({
            fillStyle: 'rgb(101, 105, 108)',
            p1:{
              type:'line',
              x1: jiapan_x+0, y1: pya,
              x2: jiapan_x+0, y2: pyb,
              x3: jiapan_x+zxp_b, y3: pyb,
              x4: jiapan_x+zxp_b, y4: pya,
            }
          });
          $('#main_view').drawPath({
            fillStyle: 'rgb(121, 125, 128)',
            p1:{
              type:'line',
              x1:jiapan_x+0,y1:pya,
              x2:jiapan_x+0,y2:pyc,
              x3:jiapan_x+zxp_b,y3:pyc,
              x4:jiapan_x+zxp_b,y4:pya,
            }
          });
        }

        if(pya>pyb&&pya>((height/2)+center_wheel_r)){
          $('#main_view').drawPath({
            fillStyle: 'rgb(121, 125, 128)',
            p1:{
              type:'line',
              x1: jiapan_x+0, y1: (height/2)+center_wheel_r,
              x2: jiapan_x+0, y2: pya,
              x3: jiapan_x+zxp_b, y3: pya,
              x4: jiapan_x+zxp_b, y4:(height/2)+center_wheel_r,
              x5:jiapan_x+0,y5:(height/2)+center_wheel_r,
            }
          });
        }
      }
      jiapanhuizhi(pya1,pyb1,pyc1,pyd1);
      jiapanhuizhi(pya2,pyb2,pyc2,pyd2);
      jiapanhuizhi(pya3,pyb3,pyc3,pyd3);

  }

  //绘制夹盘，分成三部分，共100像素宽
  sanjiajiabanhizhi(90+workpiece_r-center_wheel_r,center_wheel_r,0,'rgb(131, 135, 138)','rgb(211, 215, 218)',50)
  sanjiajiabanhizhi(70,workpiece_r,50,'rgb(171, 175, 178)','#eee',30)
  sanjiajiabanhizhi(55,workpiece_r,80,'rgb(171, 175, 178)','#eee',20)

  //绘制尾座
  $('#main_view').drawVector({
    fillStyle:'rgb(131, 135, 138)',
      rounded: true,
      x: workpiece_l+100, y: height/2,
      a1: 60, l1: 100,
      a2: 90, l2: 200,
      a3: 180, l3: 100,
      a4: 270, l4: 200,
  });

  //绘制棒料
    function bangliaohuizhi(bangliao_d,bangliao_l,bangliao_c,b){
      $('#main_view').drawPath({
        fillStyle:
        $('canvas').createGradient({
          x1: 0, y1:  (height/2)-(bangliao_d/2),
          x2: 0, y2:  (height/2)+(bangliao_d/2),
          c1: 'rgb(171, 175, 178)',
          c2: '#eee', s2: 0.5,
          c3: 'rgb(171, 175, 178)', s3: 1
        }),
        p1:{
          type:'line',
          x1: 100, y1: (height/2)-(bangliao_d/2),
          x2: 100+(bangliao_l-bangliao_c)-0.5*b, y2: (height/2)-(bangliao_d/2),
          x3: 100+(bangliao_l-bangliao_c)-0.5*b,y3:(height/2)+(bangliao_d/2),
          x4: 100,y4:(height/2)+(bangliao_d/2),
        },
        p2:{
          type:'line',

          x1: 100+(bangliao_l-bangliao_c), y1: (height/2)-(bangliao_d/2)+b,
          x2: 100+bangliao_l, y2: (height/2)-(bangliao_d/2)+b,
          x3: 100+bangliao_l,y3:(height/2)+(bangliao_d/2)-b,
          x4: 100+(bangliao_l-bangliao_c),y4:(height/2)+(bangliao_d/2)-b,
        }
    });
      if (bangliao_c>0) {
      $('#main_view').drawPath({
        fillStyle:
        $('canvas').createGradient({
          x1: 0, y1: (height/2)-(bangliao_d/2),
          x2: 0, y2: (height/2)+(bangliao_d/2),
          c1: 'rgb(171, 55, 55)',
          c2: '#eee', s2: 0.5,
          c3: 'rgb(171, 55, 55)', s3: 1
        }),

        p1:{
          type:'line',
          x1: 100+(bangliao_l-bangliao_c)-0.5*b, y1: (height/2)-(bangliao_d/2),
          x2: 100+(bangliao_l-bangliao_c), y2: (height/2)-(bangliao_d/2)+b,
          x3: 100+(bangliao_l-bangliao_c),y3:(height/2)+(bangliao_d/2)-b,
          x4: 100+(bangliao_l-bangliao_c)-0.5*b,y4:(height/2)+(bangliao_d/2),
        },
    });
    }
  }

  bangliaohuizhi(workpiece_r*2,workpiece_l,fabrication_length,cutting_depth)

  //绘制车刀
  function chedao(x,y){
    //x，y是车刀刀尖的位置

    //绘制刀架
    $('#main_view').drawVector({
    fillStyle: 'rgb(81, 85, 88)',
    name:'daojia',
    rounded: true,
    // closed: true,
    x: x, y: y,
    a1: 205, l1: 25,
    a2: 105, l2: 3,
    a3: 180, l3: 60,
    a4: 90, l4: 50,
    a5: 0, l5: 70,
    a6: 285, l6: 45,
    a7:180,l7:160,
    a8:90,l8:43,
    a9:0,l9:120,
    });
    //绘制刀片
    $('#main_view').drawVector({
    fillStyle: 'rgb(180, 180, 0)',
    name:'knife',
    rounded: true,
    // closed: true,
    x: x, y: y,
    a1: 205, l1: 25,
    a2: 105, l2: 25,
    a3: 25, l3: 25,
    });

  }

  chedao((workpiece_l+110-knife_displacement),(height/2+workpiece_r-cutting_depth));



}

//_______________________________________________________________________________
//右视图
function right_view(workpiece_r,workpiece_l,fabrication_length,cutting_depth){
  // 清空画布
    $('#r_view').clearCanvas();

    //绘制网格
    $('#r_view').drawRect({
      fillStyle: 'rgb(20, 20, 30)',
      fromCenter:false,
      x: 0, y: 0,
      width: 1000,
      height: 500
    });
    for (var s = 0;s <1000;s=s+10) {
      $('#r_view').drawVector({
        strokeStyle: '#fff',
        strokeWidth: 0.1,
        x: 0, y: s,
        a1: 90, l1: 1000
      });
      $('#r_view').drawVector({
        strokeStyle: '#fff',
        strokeWidth: 0.1,
        x: s, y: 0,
        a1: 180, l1: 1000
      });
    }
    //画夹具中心盘
    $('#r_view').drawArc({
    fillStyle: 'rgb(131, 135, 138)',
    x: (height)/2, y: (height)/2,
    radius: center_wheel_r,
    });

    //三爪夹盘
    h=workpiece_r+40;
    o1=(basic_angle-60)* angle_xishu;
    o2=(basic_angle+60)* angle_xishu;
    o3=(basic_angle+180)* angle_xishu;

    $('#r_view').drawRect({
    fillStyle: 'rgb(101, 105, 108)',
    x: height/2+h*Math.sin(o1), y: height/2+h*Math.cos(o1),
    width: d,
    height: 80,
    rotate: (basic_angle-60)*(-1),
    }).drawRect({
    fillStyle: 'rgb(101, 105, 108)',
    x:  height/2+h*Math.sin(o2), y:  height/2+h*Math.cos(o2),
    width: d,
    height: 80,
    rotate: (basic_angle+60)*(-1),
    }).drawRect({
    fillStyle: 'rgb(101, 105, 108)',
    x:   height/2+h*Math.sin(o3), y:  height/2+h*Math.cos(o3),
    width: d,
    height: 80,
    rotate: (basic_angle+180)*(-1),
    });

    //画棒料
    $('#r_view').drawArc({
    fillStyle: 'rgb(171, 175, 178)',
    x: (height)/2, y: (height)/2,
    radius: workpiece_r,
    });
    if (fabrication_length>1) {
      $('#r_view').drawArc({
      fillStyle: 'rgb(171, 55, 55)',
      x: (height)/2, y: (height)/2,
      radius: workpiece_r,
      });
    }

    $('#r_view').drawArc({
    fillStyle: 'rgb(171, 175, 178)',
    x: (height)/2, y: (height)/2,
    radius: workpiece_r-cutting_depth,
    });

    r_chedao(height/2-workpiece_r+cutting_depth,height/2);
    function r_chedao(x,y){
      //x，y是车刀刀尖的位置

      //绘制刀架
      $('#r_view').drawVector({
      fillStyle: 'rgb(81, 85, 88)',
      name:'daojia',
      rounded: true,
      // closed: true,
      x: x-3, y: y+2,
      a1: 270, l1: 60,
      a2: 180, l2: 5,
      a3: 270, l3: 100,
      a4:180,l4:20,
      a5:90,l5:100,
      a6:180,l6:5,
      a7:90,l7:60,
      });
      //绘制刀片
      $('#r_view').drawVector({
      fillStyle: 'rgb(180, 180, 0)',
      name:'knife',
      rounded: true,
      // closed: true,
      x: x, y: y,
      a1: 270, l1: 25,
      a2: 180, l2: 6,
      a3: 90, l3: 25,
      });
    }
}

//_______________________________________________________________________________
//文字
function text_view(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius){

    //只有开始加工时，才会有切削力、温度和表面粗糙度
    if (fabrication_length>0&&(rot_speed-rot_speed_view)<0.01&&knife_displacement<=(workpiece_l-20)) {
        cutting_force=parseFloat(cutting_force).toFixed(1);
        cutting_temp=parseFloat(cutting_temp).toFixed(1);
        cutting_r=parseFloat(cutting_r).toFixed(3);
    }
    else {
        cutting_force=0;
        cutting_temp="--";
        cutting_r="--";
    }
    var xianshicanshu ="--"
    if (cut_cal_status=="force") {
        xianshicanshu="切削力："+cutting_force+" N"
    }
    if (cut_cal_status=="temp") {
        xianshicanshu="切削温度："+cutting_temp+" °C"
    }
    if (cut_cal_status=="r") {
        xianshicanshu="表面粗糙度："+cutting_r
    }

    render_text="";
    render_text+=("\n机床主轴实时转速："+rot_speed_view.toFixed(1)+" r/min\n\n");
    render_text+=("工件已被加工长度："+fabrication_length.toFixed(1)+" mm\n\n");
    render_text+=("工件半径："+workpiece_r+"mm\n\n");
    render_text+=("进给量："+feed_rate+"mm/r\n\n");
    render_text+=("背吃刀量："+cutting_depth+"mm\n\n");

    // 清空画布
    $('#text').clearCanvas();

    //绘制网格
    $('#text').drawRect({
      fillStyle: 'rgb(20, 20, 30)',
      fromCenter:false,
      x: 0, y: 0,
      width: 1000,
      height: 500
    });
    $('#text').drawText({
    fillStyle: 'rgb(152, 160, 174)',
    fromCenter: false,
    align: 'left',
        x: 10, y: 10,
        fontSize: 20,
        fontFamily: "微软雅黑",
        text: render_text,
    });
    $('#text').drawText({
    fillStyle: 'rgb(197, 136, 84)',
    fromCenter: false,
    align: 'left',
        x: 10, y: 230,
        fontSize: 30,
        fontFamily: "微软雅黑",
        text: xianshicanshu,
    });




}
