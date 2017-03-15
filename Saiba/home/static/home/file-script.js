$(function () {
    $("#id_icon").change(function (e) {
        $('.custom-file-field').html($('#id_icon').val());
    });

    $(".custom-file-control").click(function (e) {
        $('.form-control-file').trigger('click');
    });
});