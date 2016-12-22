$(function () {
    $('#search').keyup(function () {

        $('#search-results').show();

        $.ajax({
            type: "POST",
            url: "/pesquisar-ajax/",
            data: {
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
}