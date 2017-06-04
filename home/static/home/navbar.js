$(function () {
    $('#navbar-search').focusin(function () {
        $('#navbar-search-results').show();

        $('#navbar-search').keypress(function (e) {
            if (e.keyCode == 27) {
                $('#navbar-search-results').hide();
            }
        });
    });

    $('#navbar-search').focusout(function () {
        window.setTimeout(function () { $('#navbar-search-results').hide() }, 100);
    });

    $('#navbar-search').keyup(function () {
        $.ajax({
            type: "GET",
            url: "/pesquisar-navbar/?q=" + $('#navbar-search').val(),
            success: navbarSearchSuccess,
            dataType: 'html'
        });
    });
});

function navbarSearchSuccess(data, textStatus, jqXHR) {
    $('#navbar-search-results').html(data);
}