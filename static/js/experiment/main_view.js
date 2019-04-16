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
var height=1600;
//夹盘中心盘半径
var center_wheel_r=480;
 //夹盘宽度
var d=80;



//主切削力
cutting_force=0;
cutting_temp=0;
cutting_r=0;
diameter=0;

//_______________________________________________________________________________
//停止渲染
function stop_render(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid){
      machine_status=0;
      count_stop=0;
      shijianchuo=(new Date()).valueOf();

      if (brc) {
        clearTimeout(brc);
      }

    //重复调用渲染函数
      function render(){

        rendering(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid);

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
function start_render(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid){
  machine_status=1;
  count=0;
  shijianchuo=(new Date()).valueOf();

  //重复调用渲染函数
  function render(){
    rendering(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid);
    brc=setTimeout(render,1);
  }
  render();

}

//_______________________________________________________________________________
//渲染函数
function rendering(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid){
  //获取每一帧的参数计算结果 实时转速 加工长度 基准角度
  var frame=frame_cal(feed_rate,rot_speed,workpiece_l);

  vertical_view(workpiece_r,workpiece_l,fabrication_length,cutting_depth);
  right_view(workpiece_r*4,workpiece_l*4,fabrication_length*4,cutting_depth*4);
  text_view(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid);
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
        fabrication_length=knife_displacement-10
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
    width: 10000,
    height: 5000
  });
  //绘制网格

  for (var s = 0;s <10000;s=s+20) {
    $('#main_view').drawVector({
      strokeStyle: '#fff',
      strokeWidth: 0.5,
      x: 0, y: s,
      a1: 90, l1: 10000
    });
    $('#main_view').drawVector({
      strokeStyle: '#fff',
      strokeWidth: 0.5,
      x: s, y: 0,
      a1: 180, l1: 10000
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
  sanjiajiabanhizhi(360+workpiece_r*4-center_wheel_r,center_wheel_r,0,'rgb(131, 135, 138)','rgb(211, 215, 218)',200)
  sanjiajiabanhizhi(280,workpiece_r*4,200,'rgb(171, 175, 178)','#eee',120)
  sanjiajiabanhizhi(220,workpiece_r*4,320,'rgb(171, 175, 178)','#eee',80)

  //绘制尾座
  $('#main_view').drawVector({
    fillStyle:'rgb(131, 135, 138)',
      rounded: true,
      x: workpiece_l*4+400, y: height/2,
      a1: 60, l1: 400,
      a2: 90, l2: 800,
      a3: 180, l3: 400,
      a4: 270, l4: 800,
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
          x1: 400, y1: (height/2)-(bangliao_d/2),
          x2: 400+(bangliao_l-bangliao_c)-0.5*b, y2: (height/2)-(bangliao_d/2),
          x3: 400+(bangliao_l-bangliao_c)-0.5*b,y3:(height/2)+(bangliao_d/2),
          x4: 400,y4:(height/2)+(bangliao_d/2),
        },
        p2:{
          type:'line',

          x1: 400+(bangliao_l-bangliao_c), y1: (height/2)-(bangliao_d/2)+b,
          x2: 400+bangliao_l, y2: (height/2)-(bangliao_d/2)+b,
          x3: 400+bangliao_l,y3:(height/2)+(bangliao_d/2)-b,
          x4: 400+(bangliao_l-bangliao_c),y4:(height/2)+(bangliao_d/2)-b,
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
          x1: 400+(bangliao_l-bangliao_c)-0.5*b, y1: (height/2)-(bangliao_d/2),
          x2: 400+(bangliao_l-bangliao_c), y2: (height/2)-(bangliao_d/2)+b,
          x3: 400+(bangliao_l-bangliao_c),y3:(height/2)+(bangliao_d/2)-b,
          x4: 400+(bangliao_l-bangliao_c)-0.5*b,y4:(height/2)+(bangliao_d/2),
        },
    });
    }
  }

  bangliaohuizhi(workpiece_r*8,workpiece_l*4,fabrication_length*4,cutting_depth*4)

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
    a1: 205, l1: 100,
    a2: 105, l2: 12,
    a3: 180, l3: 240,
    a4: 90, l4: 200,
    a5: 0, l5: 280,
    a6: 285, l6: 180,
    a7:180,l7:640,
    a8:90,l8:172,
    a9:0,l9:480,
    });
    //绘制刀片
    $('#main_view').drawVector({
    fillStyle: 'rgb(180, 180, 0)',
    name:'knife',
    rounded: true,
    // closed: true,
    x: x, y: y,
    a1: 205, l1: 100,
    a2: 105, l2: 100,
    a3: 25, l3: 100,
    });

  }

  chedao((workpiece_l*4+110*4-knife_displacement*4),(height/2+workpiece_r*4-cutting_depth*4));



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
      width: 2000,
      height: 5000
    });
    for (var s = 0;s <2000;s=s+20) {
      $('#r_view').drawVector({
        strokeStyle: '#fff',
        strokeWidth: 0.5,
        x: 0, y: s,
        a1: 90, l1: 2000
      });
      $('#r_view').drawVector({
        strokeStyle: '#fff',
        strokeWidth: 0.5,
        x: s, y: 0,
        a1: 180, l1: 2000
      });
    }
    //画夹具中心盘
    $('#r_view').drawArc({
    fillStyle: 'rgb(131, 135, 138)',
    x: (height)/2, y: (height)/2,
    radius: center_wheel_r,
    });

    //三爪夹盘
    h=workpiece_r+160;
    o1=(basic_angle-60)* angle_xishu;
    o2=(basic_angle+60)* angle_xishu;
    o3=(basic_angle+180)* angle_xishu;

    $('#r_view').drawRect({
    fillStyle: 'rgb(101, 105, 108)',
    x: height/2+h*Math.sin(o1), y: height/2+h*Math.cos(o1),
    width: d,
    height: 320,
    rotate: (basic_angle-60)*(-1),
    }).drawRect({
    fillStyle: 'rgb(101, 105, 108)',
    x:  height/2+h*Math.sin(o2), y:  height/2+h*Math.cos(o2),
    width: d,
    height: 320,
    rotate: (basic_angle+60)*(-1),
    }).drawRect({
    fillStyle: 'rgb(101, 105, 108)',
    x:   height/2+h*Math.sin(o3), y:  height/2+h*Math.cos(o3),
    width: d,
    height: 320,
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
      x: x-12, y: y+8,
      a1: 270, l1: 240,
      a2: 180, l2: 20,
      a3: 270, l3: 400,
      a4:180,l4:80,
      a5:90,l5:400,
      a6:180,l6:20,
      a7:90,l7:240,
      });
      //绘制刀片
      $('#r_view').drawVector({
      fillStyle: 'rgb(180, 180, 0)',
      name:'knife',
      rounded: true,
      // closed: true,
      x: x, y: y,
      a1: 270, l1: 100,
      a2: 180, l2: 24,
      a3: 90, l3: 100,
      });
    }
}

//_______________________________________________________________________________
//文字
function text_view(expoeration_order,workpiece_material,workpiece_r,workpiece_l,cutting_depth,feed_rate,rot_speed,tool_cutting_edge_angle,tool_minor_cutting_edge_angle,tool_cutting_edge_inclination_angle,rake_angle,clearance_angle,minor_clearance_angle,corner_radius,cutting_fluid){
    //切削液参数
     cutting_fluid_arg=0.3;
    // n_cutting_fluid=cutting_fluid || 0;
    // if(n_cutting_fluid=='water_based_cutting_fluid'){
    //     cutting_fluid_arg=0.1
    // }
    // else if(n_cutting_fluid=='oil_based_cutting_fluid'){
    //     cutting_fluid_arg=0.5
    // }

    //只有开始加工时，才会有切削力、温度和表面粗糙度
    if (fabrication_length>0&&(rot_speed-rot_speed_view)<0.01&&knife_displacement<=(workpiece_l-20)) {
        cutting_force=parseFloat(cutting_force).toFixed(1);

        cutting_temp=parseFloat(cutting_temp).toFixed(1);

        cutting_r1=(parseFloat(cutting_r)*1000.0).toFixed(0);


        diameter=parseFloat(diameter).toFixed(3);
    }
    else {
        cutting_force=0;
        cutting_temp="--";
        cutting_r1="--";
        diameter="--"
    }
    var xianshicanshu ="--"
    if (cut_cal_status=="force") {
        xianshicanshu="切削力："+cutting_force+" N"
    }
    if (cut_cal_status=="temp") {
        xianshicanshu="切削温度："+cutting_temp+" °C"
    }
    if (cut_cal_status=="r") {
        // alert(cutting_r1);
        // alert(cutting_r1);
        xianshicanshu="表面粗糙度："+cutting_r1+" µm"
        // xianshicanshu=cutting_r;
    }
    if (cut_cal_status=="d") {
        xianshicanshu="加工精度：h7\n\n刀尖处工件直径："+diameter+" mm"
    }



    render_text="";
    render_text+=("\n工件已被加工长度："+fabrication_length.toFixed(1)+" mm\n\n");
    render_text+=("机床主轴实时转速："+rot_speed_view.toFixed(1)+" r/min\n\n");
    render_text+=("工件材料："+workpiece_material+" \n\n");
    render_text+=("工件直径："+workpiece_r*2+"mm\n\n");
    render_text+=("进给量："+feed_rate+"mm/r\n\n");
    render_text+=("背吃刀量："+cutting_depth+"mm\n\n");
    render_text+=("刀具材料："+"硬质合金（YT15） \n\n");
    render_text+=("刀具主偏角："+tool_cutting_edge_angle+"°\n\n");
    render_text+=("刀具副偏角："+tool_minor_cutting_edge_angle+"°\n\n");
    render_text+=("刀具刃倾角："+tool_cutting_edge_inclination_angle+"°\n\n");
    render_text+=("刀具前角："+rake_angle+"°\n\n");
    render_text+=("刀具后角："+clearance_angle+"°\n\n");
    render_text+=("刀具副刃后角："+minor_clearance_angle+"°\n\n");
    render_text+=("刀具刀尖圆弧半径："+corner_radius+"mm\n\n");
    if(cutting_fluid=="water_based_cutting_fluid"){
        render_text+=("加工条件："+"水基切削液\n\n");
    }
    else if(cutting_fluid=="oil_based_cutting_fluid"){
        render_text+=("加工条件："+"油基切削液\n\n");
    }
    else {
        render_text+=("加工条件："+"无切削液\n\n");
    }




    // 清空画布
    $('#text').clearCanvas();

    //绘制网格
    $('#text').drawRect({
      fillStyle: 'rgb(20, 20, 30)',
      fromCenter:false,
      x: 0, y: 0,
      width: 2000,
      height: 2000
    });
    $('#text').drawText({
    fillStyle: 'rgb(255, 255, 255)',
    fromCenter: false,
    align: 'left',
        x: 40, y: 40,
        fontSize: 48,
        fontFamily: "微软雅黑",
        text: render_text,
    });
    $('#text').drawText({
    fillStyle: 'rgb(197, 136, 84)',
    fromCenter: false,
    align: 'left',
        x: 720, y: 1332,
        fontSize: 64,
        fontFamily: "微软雅黑",
        text: xianshicanshu,
    });

    stunumber=$("#stunumber").val();
    stuname=$("#stuname").val();
    $('#text').drawText({
    fillStyle: 'rgb(80, 80, 80)',
    fromCenter: false,
    align: 'left',
        x: 920, y: 100,
        fontSize: 64,
        fontFamily: "微软雅黑",
        text: "姓名："+stuname+"\n\n学号："+ stunumber,
    });



}
