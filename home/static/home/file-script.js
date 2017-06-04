$(function () {
    buttons_css()

    $('#custom-link-button').trigger('click');

    $("#id_icon").change(function (e) {
        $('#custom-file-field').html($('#id_icon').val());
    });

    $('#custom-link-button').on('click', function () {
        $('#id_icon').val('');
        $('#custom-file-field').text('');

        document.getElementById('custom-file-field').style.display = "none";
        document.getElementById('custom-link-field').style.display = "block";
    });

    $('#custom-file-button').on('click', function () {
        $('.form-control-file').trigger('click');

        $('#custom-link-field').val('');

        document.getElementById('custom-link-field').style.display = "none";
        document.getElementById('custom-file-field').style.display = "block";
    });
});

function buttons_css() {
    custom_link_button_normal = "#5cb85c"
    custom_link_button_over = "#449d44"
    custom_link_button_pressed = "#388138"

    custom_link_button_current = custom_link_button_normal

    custom_file_button_normal = "#337ab7"
    custom_file_button_over = "#286090"
    custom_file_button_pressed = "#1f4a6f"

    custom_file_button_current = custom_file_button_normal

    $('#custom-file-button').on('mouseenter', function () {
        if (custom_file_button_current == custom_file_button_normal) {
            $('#custom-file-button').css('background-color', custom_file_button_over);
        }
    });

    $('#custom-file-button').on('mouseleave', function () {
        $('#custom-file-button').css('background-color', custom_file_button_current);
    });

    $('#custom-link-button').on('mouseenter', function () {
        if (custom_link_button_current == custom_link_button_normal) {
            $('#custom-link-button').css('background-color', custom_link_button_over);
        }
    });

    $('#custom-link-button').on('mouseleave', function () {
        $('#custom-link-button').css('background-color', custom_link_button_current);
    });

    $('#custom-file-button').on('click', function () {
        custom_file_button_current = custom_file_button_pressed
        $('#custom-file-button').css('background-color', custom_file_button_current);
        $('#custom-file-button').css('border-color', '#204d74');

        custom_link_button_current = custom_link_button_normal
        $('#custom-link-button').css('background-color', custom_link_button_current);
        $('#custom-link-button').css('border-color', '#4cae4c');
    });

    $('#custom-link-button').on('click', function () {
        custom_file_button_current = custom_file_button_normal
        $('#custom-file-button').css('background-color', custom_file_button_current);
        $('#custom-file-button').css('border-color', '#2e6da4');

        custom_link_button_current = custom_link_button_pressed
        $('#custom-link-button').css('background-color', custom_link_button_current);
        $('#custom-link-button').css('border-color', '#398439');
    });
}