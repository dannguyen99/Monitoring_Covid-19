function numberWithCommas(number) {
    x = number.innerHTML
    number.innerHTML = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function get_last_update() {
    $.ajax({
        url: '/last_update',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            last_update = new Date(data.last_update);
            var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', seccond: 'numeric'};
            last_update = last_update.toLocaleDateString("en-US", options);
            document.getElementById('last_update').innerHTML = "Last update at " + last_update;
        },
        failure: function (data) {
            alert(data.message);
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.number_with_commas').forEach(numberWithCommas);
    get_last_update();
});


