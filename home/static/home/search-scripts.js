﻿$(function () {
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
            if (e.keyCode == 188) {
                var tag_to_search = $('#search-tags').val().split(',').join('');
                tag_to_search = tag_to_search.trim();

                if (tag_to_search != '')
                    selectedTag(tag_to_search)
            }
        });
    });

    $('#search-tags').focusout(function () {
        window.setTimeout(function () { $('#search-tag-results').hide() }, 100);
    });

    $('#search-entries').keyup(function (e) {
        $('#search-entry-results').show();

        $.ajax({
            type: "GET",
            url: window.location.origin + "/pesquisar-entrada/?q=" + $('#search-entries').val(),
            success: searchEntrySuccess,
            dataType: 'html'
        });
    });

    $('#search-tags').keyup(function (e) {
        if (e.keyCode == 188) {
            $('#search-tags').val('');
        }
        else {
            $.ajax({
                type: "GET",
                url: window.location.origin + "/pesquisar-tag/?q=" + $('#search-tags').val(),
                success: searchTagSuccess,
                dataType: 'html'
            });
        }
    });
    
    // Because .click doesn't work on span
    $(".search-tag-display").on('click', '#remove-tag', function (e) {
        var tag_data = $(this).attr('tag-data');
        $('.search-tag-display ul li[tag-data=' + tag_data + ']').remove();
    });

    $('.submit-media').click(function () {
        $('#tags-selected').val('');
        $('.search-tag-display ul li').each(function () {
            $('#tags-selected').val($('#tags-selected').val() + ',' + $(this).attr('tag-data'));
        });
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

function selectedTag(tagString) {
    $('.search-tag-display ul').append('<li tag-data="' + tagString + '">' + '<span id="remove-tag-visual">' + tagString + ' <span id="remove-tag" tag-data=' + tagString + ' class="glyphicon glyphicon-remove"></span>' + '</span>' + '</li>');
    $('#search-tags').val('');
}