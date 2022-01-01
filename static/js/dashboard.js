function plot(datas) {
  datas =  eval('(' + to_json(datas) + ')');

  let pv_datas = datas['pv'];
  let browser_datas = datas['browser'];
  let os_datas = datas['os'];
  let mobile_datas = datas['mobile'];
  let net_datas = datas['net'];
  let puv_datas = datas['puv'];
  let map_datas = datas['map'];
  plot_pv_pie(pv_datas);

  let os_pie = document.getElementById("os_pie");
  let browser_pie = document.getElementById("browser_pie");
  let mobile_pie = document.getElementById("mobile_pie");
  let net_pie = document.getElementById("net_pie");

  plot_pie(os_pie, os_datas, '客户端操作系统');
  plot_pie(browser_pie, browser_datas, '客户端浏览器');
  plot_pie(mobile_pie, mobile_datas, '客户端手机');
  plot_pie(net_pie, net_datas, '网络运营商');

  plot_line(puv_datas);
  plot_map(map_datas);
}

function sum(arr) {
    return eval(arr.join("+"));
}

function to_json(str) {
  let temp = "";
  temp = str.replace(/&amp;/g,"&");
  temp = temp.replace(/&nbsp;/g," ");
  temp = temp.replace(/&#39;/g,"\'");
  temp = temp.replace(/&#34;/g,"\"");
  temp = temp.replace(/&quot;/g,"\"");
  return temp;
}

function plot_pv_pie(datas) {
  let pie = document.getElementById("pv_pie");
  let pie_chart = echarts.init(pie);
  let pie_option = {
    title: {
      text: '累计PV: ' + sum(datas),
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    // legend: {
    //   orient: 'vertical',
    //   left: 'left'
    // },
    series: [
      {
        type: 'pie',
        radius: '70%',
        center: ['50%', '50%'],
        data: [
          {value: datas[1], name: '查询回答'},
          {value: datas[0], name: '查询评论'},
          {value: datas[5], name: '查询相似度'},
          {value: datas[2], name: '查询关键词'},
          {value: datas[7], name: '评论详情'},
          {value: datas[3] + datas[6], name: '留言板'},
          {value: datas[4], name: '教程'},
          // {value: datas[8], name: '数据看板'}
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  pie_chart.clear();
  pie_chart.setOption(pie_option);
  pie_chart.resize();
}

function plot_pie(obj, data, title) {
  let pie_chart = echarts.init(obj);
  let pie_option = {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    // legend: {
    //   orient: 'vertical',
    //   left: 'left'
    // },
    series: [
      {
        type: 'pie',
        radius: '70%',
        center: ['50%', '50%'],
        data: data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  pie_chart.clear();
  pie_chart.setOption(pie_option);
  pie_chart.resize();
}

function plot_line(datas) {
  let puv_line = document.getElementById("puv_line");
  let puv_chart = echarts.init(puv_line);
  line_option = {
        title: {
            text: 'PV/UV Line',
            x: 'center'
        },
        tooltip: {
            axisPointer: {
                type: 'cross'
            }
        },
        color: ['orange', 'blue'],
        legend: {
            data: ['pv', 'uv'],
            x: 'center',
            y: 30,
            icon: 'line'
        },
        grid: {
            left: '3%',
            right: '4%',
            containLabel: true
        },
        xAxis: {
            gridIndex: 0,
            type: 'category',
            boundaryGap: false,
            splitLine: {show: false},
            data: datas['xaxis']
        },
        yAxis: [{
            gridIndex: 0,
            name: 'pv',
            splitLine: {show: false},
            type: 'value'
        },
        {
            gridIndex: 0,
            name: 'uv',
            splitLine: {show: false},
            type: 'value'
        }],
        series: [{
            name: 'pv',
            type: 'line',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: datas['pv']
        },
        {
            name: 'uv',
            type: 'line',
            xAxisIndex: 0,
            yAxisIndex: 1,
            data: datas['uv']
        }]
    };
  puv_chart.clear();
  puv_chart.setOption(line_option);
  puv_chart.resize();
}

async function plot_map(datas) {
    let screen_width = window.screen.width;
    let china = document.getElementById("china");
    china.style['height'] = screen_width + 'px';
    let map_chart = echarts.init(china);
    let allCode = await getGeoJson('all.json');
    let chinaGeoJson = await getGeoJson('100000.json');
    initEcharts(chinaGeoJson, '全国', map_chart, allCode, datas);

    function initEcharts(geoJson, name, chart, alladcode, accessData) {
        echarts.registerMap(name, geoJson);
        let option = {
            title: {
                text: name + ' PV 数据',
                x: 'center',
                y: 30
            },
            tooltip: {
                formatter: function (params) {
                    return params.name + '：' + getKey(accessData, params.name).value
                }
            },
            series: [{
                x: 'center',
                y: 50,
                type: 'map',
                map: name,
                itemStyle: {
                    areaColor: '#03befd'
                }
            }]
        }
        chart.setOption(option);
        // 解绑click事件
        chart.off("click");
        //给地图添加监听事件
        chart.on('click', params => {
            let clickRegionCode = alladcode.filter(areaJson => areaJson.name === params.name)[0].adcode;
            let clickAccessData = getKey(accessData, params.name).child;
            getGeoJson(clickRegionCode + '.json').then(regionGeoJson => initEcharts(regionGeoJson, params.name, chart, alladcode, clickAccessData))
                .catch(err => {
                    getGeoJson('100000.json').then(
                        chinaGeoJson => initEcharts(chinaGeoJson, '全国', chart, alladcode, datas)
                    )
                })
        })
    }
}

function getKey(j, key) {
    if (j != null && j.hasOwnProperty(key)) {
        return j[key];
    } else {
        return {"value": 0, "child": null};
    }
}

async function getGeoJson(jsonName) {
    return await $.get('static/map/' + jsonName);
}
