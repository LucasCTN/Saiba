$(function () {
    var justKeyDown = false;

    $('#search-entries').focusin(function () {
        if ($('#search-entries').val() != ''){
            $('#search-entry-results').show();
        }

        $('#search-entries').keypress(function (e) {
            if (e.keyCode == 27) {
                $('#search-entry-results').hide();
            }
        });
    });

    $('#search-entries').focusout(function () {
        window.setTimeout(function () { $('#search-entry-results').hide() }, 100);
    });

    $('#search-tags').focusin(function () {
        $('#search-tag-results').show();

        $('#search-tags').keypress(function (e) {
            if (e.keyCode == 27) {
                $('#search-tag-results').hide();
            }
        });

        $('#search-tags').keydown(function (e) {
            if (e.keyCode == 188 && !justKeyDown) {
                selectedTag($('#search-tags').val())
            }

            justKeyDown = true;
        });
    });

    $('#search-tags').focusout(function () {
        window.setTimeout(function () { $('#search-tag-results').hide() }, 100);
    });

    $('#search-entries').keyup(function (e) {
        $('#search-entry-results').show();

        $.ajax({
            type: "GET",
            url: "../pesquisar-entradas/?q=" + $('#search-entries').val(),
            success: searchEntrySuccess,
            dataType: 'html'
        });
    });

    $('#search-tags').keyup(function (e) {
        justKeyDown = false;

        if (e.keyCode == 188) {
            $('#search-tags').val('');
        }
        else {
            $.ajax({
                type: "GET",
                url: "../pesquisar-tags/?q=" + $('#search-tags').val(),
                success: searchTagSuccess,
                dataType: 'html'
            });
        }
    });
});

function searchEntrySuccess(data) {
    $('#search-entry-results').html(data);

    $('.entries-result').click(function (event) {
        $('#search-entries').val($(event.target).text().trim());
    });
}

function searchTagSuccess(data) {
    $('#search-tag-results').html(data);

    $('.tags-result').click(function (event) {
        selectedTag($(event.target).text());
    });
}

function selectedTag(tag) {
    var tagString = tag.trim();

    $('.search-tag-display ul').append('<li>' + tagString + '</li>');
    $('#tags-selected').val($('#tags-selected').val() + ',' + tagString);
    $('#search-tags').val('');
}