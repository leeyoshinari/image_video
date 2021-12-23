function plot_pie(total, datas) {
  let pie = document.getElementById("pie");
  let pie_chart = echarts.init(pie);
  datas =  eval('(' + datas + ')');
  let pie_option = {
    title: {
      text: '网站PV: 累计访问量 ' + total + ' 次',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: 'Access From',
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
          {value: datas[8], name: '数据看板'}
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
