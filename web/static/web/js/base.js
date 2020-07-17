$('#dropdownMenu li').click(function () {
    $('#navbarDropdownMenuLink').html($(this).text() + '<span class="caret"></span>')
})