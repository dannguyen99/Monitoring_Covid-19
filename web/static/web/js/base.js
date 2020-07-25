function numberWithCommas(number) {
    x = number.innerHTML
    number.innerHTML = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.number_with_commas').forEach(numberWithCommas)
});

