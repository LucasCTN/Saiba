$(function () {
    var justKeyDown = false;

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

    $('#search-tags').keyup(function (e) {
        justKeyDown = false;

        if (e.keyCode == 188) {
            $('#search-tags').val('');
        }
        else
        {
            $.ajax({
                type: "GET",
                url: "../pesquisar-tags/?q=" + $('#search-tags').val(),
                success: searchTagSuccess,
                dataType: 'html'
            });
        }
    });
});

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