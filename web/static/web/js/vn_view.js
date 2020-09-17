//draw daily data
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
    legend: { position: 'right' },
  };

  var chart = new google.visualization.LineChart(document.getElementById(divId));

  chart.draw(data, options);
};

//load daily data
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

//draw age chart
function drawAgeChart(histoData) {
  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(function () { drawHistogram(histoData) });
}


function drawHistogram(histoData) {
  var data = new google.visualization.DataTable()
  data.addColumn('string', 'Patient')
  data.addColumn('number', 'Age')
  data.addRows(histoData)

  var options = {
    // hAxis: {
    //   title: 'Age',

    // },
    vAxis: {
      title: 'Count'
    },
    fontName: 'Nunito',
    fontSize: 15,
  };

  var chart = new google.visualization.Histogram(document.getElementById('age_chart'));
  chart.draw(data, options);
}

//load age data
function loadAge() {
  $.ajax({
    url: '/vietnam/api',
    data: {
      'key': 'age',
    },
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      console.log(data.data)
      drawAgeChart(data.data);
    },
    failure: (data) => {
      alert(data.message);
    }
  })
}

function drawRatePieChart(divId, data) {
  google.charts.load('current', { 'packages': ['corechart'] });
  google.charts.setOnLoadCallback(function () { drawPieChart(divId, data) });
}


function drawPieChart(divId, pieData) {

  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Type')
  data.addColumn('number', 'Cases');
  data.addRows(pieData);


  var options = {
      colors: ['#343a40', '#28a745', '#ffc107', '#dc3545', '#e83e8c', '#007bff', '#6610f2'],
      chartArea: { width: '100%', height: '90%' },
      fontName: 'Nunito',
      fontSize: 15,
  };

  var chart = new google.visualization.PieChart(document.getElementById(divId));

  chart.draw(data, options);
}

function loadRatio(key, divId) {
  $.ajax({
      url: '/index/api',
      data: {
          'key': key,
      },
      type: 'GET',
      dataType: 'json',
      success: (data) => {
          drawRatePieChart(divId, data.data);
      },
      failure: function (data) {
          alert(data.message);
      }
  })
}

//load all chart
document.addEventListener('DOMContentLoaded', () => {
  loadDaily('actives', "active_curve_chart");
  loadDaily('cases', 'case_curve_chart');
  loadAge();
});

//prepare datatable
$(document).ready(function () {
  $('#dataTable').DataTable({
    "order": [[1, 'desc']]
  });
});