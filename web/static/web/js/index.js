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
    data.addColumn('number', 'Confirmed');
    data.addRows(geochartData);

    var options = {
        title: "World Corona Virus Case by 1M pop",
        colorAxis: { colors: ['#00853f', 'black', '#e31b23'] },
        backgroundColor: '#81d4fa',
        datalessRegionColor: '#f8bbd0',
        defaultColor: '#f5f5f5',
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
        colors_l = ['gray'];
        data.addColumn('number', 'Cases');
    }
    else {
        colors_l = ['red'];
        data.addColumn('number', 'Deaths');
    }
    for (d of dailyData) {
        day = new Date(d[0])
        day.setMonth(day.getMonth() - 1)
        data.addRow([day, d[1]]);
    }

    var options = {
        backgroundColor: '#fbf9f9',
        titleTextStyle: {
            color: '#000000',
            fontName: 'Times New Roman',
            fontSize: 25,
            bold: true,
        },
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

$(document).ready(function() {
    var t = $('#dataTable').DataTable( {
        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        } ],
    } );
 
    t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );