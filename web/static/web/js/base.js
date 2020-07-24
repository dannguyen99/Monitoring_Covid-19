var arrLang = new Array();
arrLang["en"] = new Array();
arrLang["vn"] = new Array();

// English content
arrLang["en"]["references"] = "References";
arrLang["en"]["about"] = "About Us";

// VN content
arrLang["vn"]["references"] = "Tham khảo";
arrLang["vn"]["about"] = "Về chúng tôi";

// Process translation
$(function () {
    $(".translate").click(function () {
        var lang = $(this).attr("id");

        $(".lang").each(function (index, item) {
            $(this).text(arrLang[lang][$(this).attr("key")]);
        });
    });
});