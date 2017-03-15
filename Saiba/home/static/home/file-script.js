$(function () {
    $("#id_icon").change(function (e) {
        $('#custom-file-field').html($('#id_icon').val());
    });

    $(document).on('click', '.custom-file-button', function () {
        document.getElementById('custom-link-field').style.display = "none";
        document.getElementById('custom-file-field').style.display = "block";
        $('.form-control-file').trigger('click');
    });

    $(document).on('click', '.custom-link-button', function () {
        document.getElementById('custom-file-field').style.display = "none";
        document.getElementById('custom-link-field').style.display = "block";
    });
});