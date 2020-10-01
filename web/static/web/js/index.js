//draw World Map
function drawWorldMap(filter_type, geochartData) {
    if (lang === "vn")
        google.charts.load('current', {
            'packages': ['geochart'], 'language': 'vi',
            // Note: you will need to get a mapsApiKey for your project.
            // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
            'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
        });
    else
        google.charts.load('current', {
            'packages': ['geochart'],
            // Note: you will need to get a mapsApiKey for your project.
            // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
            'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
        });
    google.charts.setOnLoadCallback(function () { drawRegionsMap(filter_type, geochartData) });
}

function drawRegionsMap(filter_type, geochartData) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Country');
    data.addColumn('number', arrLang[lang][filter_type]);
    data.addRows(geochartData);
    data.addRow(['Greenland', 14])

    var options = {
        colorAxis: { colors: ['#00853f', 'black', '#e31b23'] },
        backgroundColor: '#81d4fa',
        datalessRegionColor: '#f8bbd0',
        defaultColor: '#f5f5f5',
        height: 560,
    };

    var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

    chart.draw(data, options);
};

function loadWorldMap(filter_type) {
    $.ajax({
        url: '/index/api',
        data: {
            'key': 'change_world_map',
            'filter_type': filter_type
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            drawWorldMap(filter_type, data.geochart_data)
        },
        failure: function (data) {
            alert(data.message);
        }
    })
}

// change world map filter
document.querySelectorAll('.filter').forEach(button => {
    button.onclick = () => {
        filter_type = button.getAttribute("filter_type")
        loadWorldMap(filter_type)
    }
});

//draw cases and death daily chart
function drawDaily(divId, dailyData) {
    if (lang === "vn")
        google.charts.load('current', { packages: ['corechart', 'bar'], 'language': 'vi' });
    else
        google.charts.load('current', { packages: ['corechart', 'bar'] });
    google.charts.setOnLoadCallback(function () { drawTrendlines(divId, dailyData) });
}


function drawTrendlines(divId, dailyData) {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Day');
    if (divId === 'daily_cases_chart_div') {
        colors_l = ['#dc3545'];
        data.addColumn('number', arrLang[lang]["daily_cases"]);
    }
    else {
        colors_l = ['#343a40'];
        data.addColumn('number', arrLang[lang]["daily_deaths"]);
    }
    for (d of dailyData) {
        data.addRow([new Date(d[0]), d[1]]);
    }

    var options = {
        trendlines: {
            0: { type: 'exponential', lineWidth: 4, opacity: .5 }
        },
        colors: colors_l,
        animation: {
            "startup": true,
            "duration": 3000,
            easing: 'in',
        },
        legend: { position: "in" },
        hAxis: {
            title: arrLang[lang]["date"]

        },
        vAxis: {
            title: arrLang[lang]["daily_new_cases"]
        },
        fontName: 'Nunito',
    }

    var chart = new google.visualization.ColumnChart(document.getElementById(divId));
    chart.draw(data, options);
}

//load daily chart
function loadDaily(divId, filter_type = '') {
    $.ajax({
        url: '/index/api',
        data: {
            'key': 'timeline_data',
            'language': lang,
            'filter_type': filter_type
        },
        type: 'GET',
        dataType: 'json',
        success: (data) => {
            drawDaily(divId, data.data);
        },
        failure: function (data) {
            alert(data.message);
        }
    })
}

// prepare datatable

$(document).ready(function () {
    if (lang === "vn") {
        var t = $('#dataTable').DataTable({
            "columnDefs": [{
                "searchable": false,
                "orderable": false,
                "targets": 0
            }],
            "order": [[2, 'desc']],
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Vietnamese.json"
            }
        });

        t.on('order.dt search.dt', function () {
            t.column(0, { search: 'applied', order: 'applied' }).nodes().each(function (cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    }
    else {
        var t = $('#dataTable').DataTable({
            "columnDefs": [{
                "searchable": false,
                "orderable": false,
                "targets": 0
            }],
            "order": [[2, 'desc']],
        });

        t.on('order.dt search.dt', function () {
            t.column(0, { search: 'applied', order: 'applied' }).nodes().each(function (cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    }
});


//drawRatePieChart
function drawRatePieChart(divId, data) {
    if (lang === "vn")
        google.charts.load('current', { 'packages': ['corechart'], 'language': 'vi' });
    else
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

function loadRatio(key, divId, filter_type = '') {
    $.ajax({
        url: '/index/api',
        data: {
            'key': key,
            'language': lang,
            'filter_type': filter_type
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

//change continent chart filter
document.querySelectorAll('.continent_filter').forEach(button => {
    button.onclick = () => {
        const filter_type = button.getAttribute("filter_type")
        loadRatio("continent", "piechart_region_ratio", filter_type)
    }
});

document.addEventListener('DOMContentLoaded', (event) => {
    loadDaily('daily_cases_chart_div', 'cases')
    loadDaily('daily_deaths_chart_div', 'deaths')
    loadWorldMap('total_cases')
    loadRatio("case_ratio", "piechart_case_ratio");
    loadRatio("continent", "piechart_region_ratio", 'total_cases')
});