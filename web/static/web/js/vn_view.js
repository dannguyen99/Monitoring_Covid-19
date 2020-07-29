function drawCurveChart(divId, curveData) {
  google.charts.load('current', { 'packages': ['corechart'] });
  google.charts.setOnLoadCallback(function () { drawChart(divId, curveData) });
}


function drawChart(divId, curveData) {
  var data = new google.visualization.DataTable();
  data.addColumn('date', 'Date');
  if (divId === "active_curve_chart") {
    data.addColumn('number', 'Death');
    data.addColumn('number', 'Active');
    colors = ['red', 'orange'];
    if (lang == "vn") {
      title = "CÁC CA ĐANG ĐIỀU TRỊ VÀ TỬ VONG TÍNH THEO NGÀY";
    }
    else
      title = "Vietnam COVID-19 Daily Active and Death";
  }
  else {
    data.addColumn('number', 'Confirmed');
    data.addColumn('number', 'Recovered');
    colors = ['blue', 'green'];
    if (lang == "vn") {
      title = "CÁC CA NHIỄM MỚI VÀ ĐÃ HỒI PHỤC TÍNH THEO NGÀY";
    }
    else
      title = "Vietnam Covid 19 Daily Confirmed and Recovered";
  }

  for (d of curveData) {
    day = new Date(d[0])
    day.setMonth(day.getMonth() - 1)
    data.addRow([day, d[1], d[2]]);
  }

  var options = {
    axisTitlesPosition: 'out',
    title: title,
    titleTextStyle: {
      color: '#000000',
      fontName: 'Times New Roman',
      fontSize: 25,
      bold: true,    // true or false
      // italic: <boolean>   // true of false
    },
    colors: colors,
    curveType: 'function',
    backgroundColor: '#fbf9f9',
    legend: { position: 'right' },
  };

  var chart = new google.visualization.LineChart(document.getElementById(divId));

  chart.draw(data, options);
};

function loadDaily(filterType, divId) {
  $.ajax({
    url: '/vietnam/api',
    data: {
      'key': 'daily_data',
      'filter_type': filterType
    },
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      drawCurveChart(divId, data.data);
    },
    failure: function (data) {
      alert(data.message);
    }
  })
}

document.addEventListener('DOMContentLoaded', (event) => {
  loadDaily('actives', "active_curve_chart");
  loadDaily('cases', 'case_curve_chart');
});
