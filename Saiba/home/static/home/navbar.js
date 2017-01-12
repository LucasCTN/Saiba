$(function () {
    $('#search').focusin(function () {
        $('#search-results').show();

        $('#search').keypress(function (e) {
            if (e.keyCode == 27) {
                $('#search-results').hide();
            }
        });
    });

    $('#search').focusout(function () {
        window.setTimeout(function () { $('#search-results').hide() }, 100);
    });

    $('#search').keyup(function () {
        $.ajax({
            type: "GET",
            url: "/pesquisar-ajax/?q=" + $('#search').val(),
            success: searchEntrySuccess,
            dataType: 'html'
        });
    });
});

function searchEntrySuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
}