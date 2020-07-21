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


