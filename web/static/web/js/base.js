var arrLang = new Array();
arrLang["en"] = new Array();
arrLang["vn"] = new Array();

// English content

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
arrLang["en"]["total_cases"] = "Total cases";
arrLang["en"]["active"] = "Actives";
arrLang["en"]["recover"] = "Recovered";
arrLang["en"]["death"] = "Death";
arrLang["en"]["per_country"] = "SUMMARY OF CASES WORLDWIDE PER COUNTRIES";
arrLang["en"]["world_map"] = "COVID-19 World map";


// VN content
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
arrLang["vn"]["total_cases"] = "SỐ CA NHIỄM";
arrLang["vn"]["active"] = "ĐANG NHIỄM";
arrLang["vn"]["recover"] = "KHỎI";
arrLang["vn"]["death"] = "TỬ VONG";
arrLang["vn"]["per_country"] = "DIỄN BIẾN DỊCH Ở TỪNG NƯỚC";
arrLang["vn"]["world_map"] = "BẢN ĐỒ DIỄN BIẾN DỊCH TRÊN THẾ GIỚI";




// Process translation
$(function () {
    $(".translate").click(function () {
        var lang = $(this).attr("id");

        $(".lang").each(function (index, item) {
            $(this).text(arrLang[lang][$(this).attr("key")]);
        });
    });
});