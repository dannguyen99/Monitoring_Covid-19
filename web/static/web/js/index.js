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
document.querySelectorAll('.btn').forEach(button => {
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
        title = 'Daily New Cases';
    }
    else {
        colors_l = ['red'];
        data.addColumn('number', 'Deaths');
        title = 'Daily New Deaths';
    }
    for (d of dailyData) {
        day = new Date(d[0])
        day.setMonth(day.getMonth() - 1)
        data.addRow([day, d[1]]);
    }

    var options = {
        title: title,
        trendlines: {
            0: { type: 'exponential', lineWidth: 4, opacity: .5 }
        },
        colors: colors_l,
        animation: {
            "startup": true,
            "duration": 3000,
            easing: 'in',
        },
    }

    var chart = new google.visualization.ColumnChart(document.getElementById(divId));
    chart.draw(data, options);
}

//sort table
const getCellValue = (tr, idx) => tr.children[idx].innerText.replace(/,/g, '') || tr.children[idx].textContent.replace(/,/g, '');

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
