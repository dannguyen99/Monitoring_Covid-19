function drawChart() {
    google.charts.load('current', { 'packages': ['corechart'] });
    google.charts.setOnLoadCallback(drawChart);
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date')
    data.addColumn('number', 'Confirmed');
    data.addColumn('number', 'Death');
    data.addColumn('number', 'Active');
    data.addColumn('number', 'Recovered');

    data.addRows({{ rows| safe}});

var options = {
    title: 'Vietnam Covid 19 Cases',
    curveType: 'function',
    legend: { position: 'bottom' }
};

var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
chart.draw(data, options);
};
drawChart();
/* <script type="text/javascript">
    google.charts.load('current', {'packages': ['bar'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date')
    data.addColumn('number', 'Male');
    data.addColumn('number', 'Female');
    data.addColumn('number', 'Total');

    data.addRows({{ sexs| safe}});


  var options = {
        chart: {
        title: 'Cases by Gender',
    }
  };

  var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

  chart.draw(data, google.charts.Bar.convertOptions(options));
  }
</script>

    <script type="text/javascript">
        google.charts.load("current", {packages: ["corechart"] });
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var data = new google.visualization.DataTable()
    data.addColumn('string', 'Patient')
    data.addColumn('number', 'Age')
    data.addRows({{ ages| safe}})

  var options = {
            title: 'Age of patients, in year',
    legend: {position: 'right' },
  };

  var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
  chart.draw(data, options);
  }
</script> */