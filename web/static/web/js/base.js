var arrLang = new Array();
arrLang["en"] = new Array();
arrLang["vn"] = new Array();

// English content

// title
arrLang["en"]["title1"] = "COVID-19 OUTBREAK IN THE WORLD";
arrLang["en"]["title2"] = "Last updated at today";

// nav tab 
arrLang["en"]["region"] = "Region";
arrLang["en"]["references"] = "References";
arrLang["en"]["about"] = "About Us";
arrLang["en"]["world"] = "The World";
arrLang["en"]["us"] = "America";
arrLang["en"]["eu"] = "Europe";
arrLang["en"]["about"] = "About Us";
arrLang["en"]["change_lang"] = "Change language";

// table
arrLang["en"]["sum_world"] = "SUMMARY OF CASES WORLDWIDE";
arrLang["en"]["sum_vn"] = "Summary of Cases in Vietnam";
arrLang["en"]["sum_us"] = "Summary of Cases in US";
arrLang["en"]["sum_each"] = "Summary of Cases in";

arrLang["en"]["per_city"] = "Cases by City/Province";
arrLang["en"]["city"] = "City/Province";
arrLang["en"]["per_states"] = "Summary of Cases per States";
arrLang["en"]["states"] = "State";

arrLang["en"]["total_cases"] = "Total cases";
arrLang["en"]["active"] = "Actives";
arrLang["en"]["recover"] = "Recovered";
arrLang["en"]["death"] = "Death";
arrLang["en"]["new_case"] = "NEWS CASES";
arrLang["en"]["new_death"] = "NEW DEATH";
arrLang["en"]["per_country"] = "SUMMARY OF CASES WORLDWIDE PER COUNTRIES";
arrLang["en"]["world_map"] = "COVID-19 World map";
arrLang["en"]["vn_map"] = "COVID-19 Vietnam map";
arrLang["en"]["us_map"] = "COVID-19 America map";

arrLang["en"]["country"] = "Countries and Territories";
arrLang["en"]["cases_per_1m"] = "Total cases/1M pop";
arrLang["en"]["population"] = "Population Data 2019";

// button

arrLang["en"]["btn-cf"] = "Confirmed Cases";
arrLang["en"]["btn-pp"] = "Total cases/1M population";

// VN content

// title
arrLang["vn"]["title1"] = "Tình hình dịch bệnh COVID-19 trên thế giới";
arrLang["vn"]["title2"] = "Cập nhật lần cuối vào hôm nay";

// nav tab
arrLang["vn"]["region"] = "Khu vực";
arrLang["vn"]["references"] = "Tham khảo";
arrLang["vn"]["about"] = "Về chúng tôi";
arrLang["vn"]["world"] = "Toàn thế giới";
arrLang["vn"]["us"] = "Hoa Kỳ";
arrLang["vn"]["eu"] = "Châu Âu";
arrLang["vn"]["change_lang"] = "đổi ngôn ngữ";

// table
arrLang["vn"]["sum_world"] = "TÌNH HÌNH DỊCH BỆNH TOÀN THẾ GIỚI";
arrLang["vn"]["sum_vn"] = "TÌNH HÌNH DỊCH BỆNH Ở VIỆT NAM";
arrLang["vn"]["sum_us"] = "TÌNH HÌNH DỊCH BỆNH Ở HOA KỲ";
arrLang["vn"]["sum_each"] = "TÌNH HÌNH DỊCH BỆNH Ở";

arrLang["vn"]["per_city"] = "CA NHIỄM THEO TỈNH THÀNH";
arrLang["vn"]["city"] = "TỈNH/THÀNH PHỐ";
arrLang["vn"]["per_states"] = "CA NHIỄM THEO BANG";
arrLang["vn"]["states"] = "BANG";

arrLang["vn"]["total_cases"] = "SỐ CA NHIỄM";
arrLang["vn"]["active"] = "ĐANG NHIỄM";
arrLang["vn"]["recover"] = "KHỎI";
arrLang["vn"]["death"] = "TỬ VONG";
arrLang["vn"]["new_case"] = "CA NHIỄM MỚI";
arrLang["vn"]["new_death"] = "CA TỬ VONG MỚI";
arrLang["vn"]["per_country"] = "DIỄN BIẾN DỊCH Ở TỪNG NƯỚC";
arrLang["vn"]["world_map"] = "BẢN ĐỒ DIỄN BIẾN DỊCH TRÊN THẾ GIỚI";
arrLang["vn"]["vn_map"] = "BẢN ĐỒ DIỄN BIẾN DỊCH Ở VIỆT NAM";
arrLang["vn"]["us_map"] = "BẢN ĐỒ DIỄN BIẾN DỊCH Ở HOA KỲ";

arrLang["vn"]["country"] = "QUỐC GIA/VÙNG LÃNH THỔ";
arrLang["vn"]["cases_per_1m"] = "SỐ CA NHIỄM/1TR NGƯỜI";
arrLang["vn"]["population"] = "DÂN SỐ NĂM 2019";

// button

arrLang["vn"]["btn-cf"] = "Tổng số ca nhiễm";
arrLang["vn"]["btn-pp"] = "Số ca nhiễm/1 triệu người";


// Process translation
$(document).ready(function () {
    $(".translate").click(function () {
        var lang = $(this).attr("id");
        localStorage.setItem('language', lang);
        $(".lang").each(function (index, item) {
            $(this).text(arrLang[lang][$(this).attr("key")]);
        });
    });
    $(".lang").each(function (index, item) {
        $(this).text(arrLang[lang][$(this).attr("key")]);
    });
});

// load change language localstorage
var lang = localStorage.getItem('language');

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


