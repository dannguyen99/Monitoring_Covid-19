//draw daily data
function drawCurveChart(curveData) {
  google.charts.load('current', { 'packages': ['corechart'] });
  google.charts.setOnLoadCallback(function () { drawChart(curveData) });
}


function drawChart(curveData) {
  var data = new google.visualization.DataTable();
  data.addColumn('date', 'Date');
  data.addColumn('number', 'Confirmed Cases');
  data.addColumn('number', 'Death Cases')

  for (d of curveData) {
    day = new Date(d[0])
    data.addRow([day, d[1], d[2]]);
  }

  var options = {
    legend: { position: 'bottom' },
    series: {
      0: { targetAxisIndex: 0 },
      1: { targetAxisIndex: 1 }
    },
    fontName: 'Nunito',
    fontSize: 15,
    vAxes: {
      // Adds titles to each axis.
      0: { title: 'Confirmed Cases' },
      1: {
        title: 'Death Cases',
        format: '#,#'
      }
    },
    colors: ['#dc3545', '#343a40']
  };

  var chart = new google.visualization.LineChart(document.getElementById('daily_linechart'));
  chart.draw(data, options);
};

//load daily data
function loadDaily() {
  $.ajax({
    url: '/vietnam/api',
    data: {
      'key': 'daily_data',
    },
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      drawCurveChart(data.data);
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
    hAxis: {
      title: 'Age Range',

    },
    vAxis: {
      title: 'Number of Cases'
    },
    fontName: 'Nunito',
    fontSize: 15,
    legend: { position: 'none' }
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
      drawAgeChart(data.data);
    },
    failure: (data) => {
      alert(data.message);
    }
  })
}

//draw rate pie chart
function drawRatePieChart(data) {
  google.charts.load('current', { 'packages': ['corechart'] });
  google.charts.setOnLoadCallback(function () { drawPieChart(data) });
}


function drawPieChart(pieData) {

  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Nationality')
  data.addColumn('number', 'Cases');
  data.addRows(pieData);


  var options = {
    chartArea: { width: '100%', height: '90%' },
    fontName: 'Nunito',
    fontSize: 15,
  };

  var chart = new google.visualization.PieChart(document.getElementById('piechart_nationality'));

  chart.draw(data, options);
}

function loadRatio() {
  $.ajax({
    url: '/vietnam/api',
    data: {
      'key': 'nationality',
    },
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      drawRatePieChart(data.data);
    },
    failure: function (data) {
      alert(data.message);
    }
  })
}

//draw Gender chart
function loadGenderRatio(){
  $.ajax({
    url: '/vietnam/api',
    data: {
      'key': 'gender',
      'option': 'header',
      'language': localStorage.getItem('language')
    },
    type: 'GET',
    dataType: 'json',
    success: (returnData) => {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawGenderRateChart);

      function drawGenderRateChart() {

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Gender')
        data.addColumn('number', 'Cases');
        data.addRows(returnData.data);

        var options = {
          chartArea: { width: '100%', height: '90%' },
          fontName: 'Nunito',
          fontSize: 15,
        };

        var chart = new google.visualization.PieChart(document.getElementById('gender_piechart'));

        chart.draw(data, options);
      }
    },
    failure: function (data) {
      alert(data.message);
    }
  })
}

// draw geomap
function drawCityGeomap(data) {
  google.charts.load('current', {
    'packages': ['geochart'],
    // Note: you will need to get a mapsApiKey for your project.
    // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
    'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
  });
  google.charts.setOnLoadCallback(function () { drawGeomap(data) });
}

function drawGeomap(geoData) {
  var data = new google.visualization.DataTable();
  data.addColumn('string', "City/Province")
  data.addColumn('number', 'Confirmed')
  data.addRows(geoData)


  var options = {
    region: 'VN',
    colorAxis: { colors: ['#00853f', 'black', '#e31b23'] },
    backgroundColor: '#81d4fa',
    datalessRegionColor: '#fff',
    defaultColor: '#f5f5f5',
    resolution: "provinces",
    keepAspectRatio: false
  };

  var chart = new google.visualization.GeoChart(document.getElementById('geochart-colors'));
  chart.draw(data, options);
};

function loadGeomap() {
  $.ajax({
    url: '/vietnam/api',
    data: {
      'key': 'city_geomap',
    },
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      drawCityGeomap(data.data);
    },
    failure: function (data) {
      alert(data.message);
    }
  })
}

//load all chart
document.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('language') === "vn")
    document.getElementById('patient_summary').style.display = 'block'
  loadDaily();
  loadAge();
  loadRatio();
  loadGeomap();
  loadGenderRatio()
});

//prepare datatable
$(document).ready(function () {
  if (localStorage.getItem('language') === "vn"){
    $('#dataTable').DataTable({
      "order": [[1, 'desc']],
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Vietnamese.json"
    }
    });
    $('#patient_dataTable').DataTable({
      "aaSorting": [],
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Vietnamese.json"
    }
    });
  }
  else{
    $('#dataTable').DataTable({
      "order": [[1, 'desc']]
    });
  }
});

