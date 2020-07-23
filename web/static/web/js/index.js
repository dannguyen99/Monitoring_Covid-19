//draw World Map
function drawWorldMap(geochart_data) {
    google.charts.load('current', {
        'packages': ['geochart'],
        // Note: you will need to get a mapsApiKey for your project.
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
        'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
    });
    google.charts.setOnLoadCallback(function () { drawRegionsMap(geochart_data) });
}

function drawRegionsMap(geochart_data) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Country');
    data.addColumn('number', 'Confirmed');
    data.addRows(geochart_data);

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
document.querySelectorAll('.btn').forEach(button => {
    button.onclick = () => {
        $.ajax({
            url: '/index/change_world_map',
            data: {
                'filter_type': button.getAttribute("filter_type")
            },
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
function drawDaily(div_id, daily_data) {
    google.charts.load('current', { packages: ['corechart', 'bar'] });
    google.charts.setOnLoadCallback(function () { drawTrendlines(div_id, daily_data) });
}


function drawTrendlines(div_id, daily_data) {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Day');
    data.addColumn('number', 'Cases');

    for (d of daily_data) {
        day = new Date(d[0])
        day.setMonth(day.getMonth() - 1)
        data.addRow([day, d[1]]);
    }
    if (div_id === 'daily_cases_chart_div') {
        colors_l = ['gray'];
    }
    else {
        colors_l = ['red']
    }
    var options = {
        title: 'Daily New Cases',
        trendlines: {
            0: { type: 'exponential', lineWidth: 4, opacity: .5 }
        },
        colors: colors_l,
    }

    var chart = new google.visualization.ColumnChart(document.getElementById(div_id));
    chart.draw(data, options);
}

//sort table
const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
)(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// do the work...
document.querySelectorAll('.sort_header').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');
    Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table.appendChild(tr));
})));
