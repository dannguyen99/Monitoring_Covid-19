//draw World Map
function drawWorldMap(geochartData) {
    google.charts.load('current', {
        'packages': ['geochart'],
        // Note: you will need to get a mapsApiKey for your project.
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
        'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
    });
    google.charts.setOnLoadCallback(function () { drawRegionsMap(geochartData) });
}

function drawRegionsMap(geochartData) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Country');
    data.addColumn('number', 'Confirmed/1M');
    data.addRows(geochartData);
    data.addRow(['Greenland', 14])

    var options = {
        colorAxis: { colors: ['#00853f', 'black', '#e31b23'] },
        backgroundColor: '#81d4fa',
        datalessRegionColor: '#fff',
        defaultColor: '#f5f5f5',
        height: 560,
    };

    var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

    chart.draw(data, options);
};

// change world map filter
document.querySelectorAll('.filter').forEach(button => {
    button.onclick = () => {
        $.ajax({
            url: '/index/change_world_map',
            data: {
                'filter_type': button.getAttribute("filter_type")
            },
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                drawWorldMap(JSON.parse(data.geochart_data))
            },
            failure: function (data) {
                alert(data.message);
            }
        })
    }
});

//draw cases and death daily chart
function drawDaily(divId, dailyData) {
    google.charts.load('current', { packages: ['corechart', 'bar'] });
    google.charts.setOnLoadCallback(function () { drawTrendlines(divId, dailyData) });
}


function drawTrendlines(divId, dailyData) {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Day');
    if (divId === 'daily_cases_chart_div') {
        colors_l = ['#dc3545'];
        data.addColumn('number', 'Cases');
    }
    else {
        colors_l = ['#343a40'];
        data.addColumn('number', 'Deaths');
    }
    for (d of dailyData) {
        day = new Date(d[0])
        day.setMonth(day.getMonth() - 1)
        data.addRow([day, d[1]]);
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
        legend: { position: "in" }
    }

    var chart = new google.visualization.ColumnChart(document.getElementById(divId));
    chart.draw(data, options);
}

$(document).ready(function () {
    var t = $('#dataTable').DataTable({
        "columnDefs": [{
            "searchable": false,
            "orderable": false,
            "targets": 0
        }],
        "order": [[2, 'desc']]
    });

    t.on('order.dt search.dt', function () {
        t.column(0, { search: 'applied', order: 'applied' }).nodes().each(function (cell, i) {
            cell.innerHTML = i + 1;
        });
    }).draw();
});

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
            console.log(data.data)
            drawRatePieChart(divId, data.data);
        },
        failure: function (data) {
            alert(data.message);
        }
    })
}

document.addEventListener('DOMContentLoaded', (event) => {
    loadRatio("case_ratio", "piechart_case_ratio");
    loadRatio("who_region_new_cases", "piechart_region_ratio")
});