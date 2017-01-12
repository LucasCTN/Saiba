$(function () {
    $('#search-tags').focusin(function () {
        $('#search-tag-results').show();

        $('#search-tags').keypress(function (e) {
            if (e.keyCode == 27) {
                $('#search-tag-results').hide();
            }
        });
    });

    $('#search-tags').focusout(function () {
        window.setTimeout(function () { $('#search-tag-results').show() }, 100);
    });

    $('#search-tags').keyup(function () {
        $.ajax({
            type: "GET",
            url: "../pesquisar-tags/?q=" + $('#search-tags').val(),
            success: searchTagSuccess,
            dataType: 'html'
        });
    });
});

function searchTagSuccess(data, textStatus, jqXHR) {
    $('#search-tag-results').html(data);

    $('.tags-result').click(function (event) {
        var tag = $(event.target);

        $('.search-tag-display ul').append('<li>' + tag.text().trim() + '</li>');
    });
}