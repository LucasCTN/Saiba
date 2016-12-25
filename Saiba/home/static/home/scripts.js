function sendComment(formId, formType, formSlug, formContent, sendCommentApiEndpoint, getCommentApiEndpoint) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST",
        url: sendCommentApiEndpoint,
        data: { type: formType, slug: formSlug, content: formContent, id: formId },
        success: function (data) {
            updateCommentSection("#comment-section", getCommentApiEndpoint);

            $(document).ajaxStop(function () {
                $('html, body').animate({
                    scrollTop: $("#comment-" + data.id).offset().top
                }, 2000);
            });            
        }
    })
}

function sendReply(parentCommentId, parentReplyId, formContent, sendReplyApiEndpoint, getCommentApiEndpoint) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST",
        url: sendReplyApiEndpoint,
        data: { comment: parentCommentId, content: formContent, response_to: parentReplyId },
        success: function (data) {
            updateCommentSection("#comment-section", getCommentApiEndpoint);
        }
    })
}

function getVote(contentId, type) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "GET",
        url: voteApiEndpoint,
        data: 'type=' + type + '&id=' + contentId,
        success: function (data) {
            createCommentSection(commentSectionId, data);
        }
    })
}

function sendVote(contentId, type, direction) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST",
        url: voteApiEndpoint,
        data: { id: contentId, type: type, direction: direction },
        success: function (data) {
            updateCommentSection("#comment-section", getCommentApiEndpoint);
        }
    })
}

function updateCommentSection(commentSectionId, getCommentApiEndpoint, append_only) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "GET",
        url: getCommentApiEndpoint,
        data: $(this).serialize(),
        success: function (data) {
            if (append_only != true)
                $(commentSectionId).empty();
            createCommentSection(commentSectionId, data);
        }
    })
}

function appendCommentSection(commentSectionId, getCommentApiEndpoint) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "GET",
        url: getCommentApiEndpoint,
        data: $(this).serialize(),
        success: function (data) {
            createCommentSection(commentSectionId, data);
        }
    })
}

function createCommentChain(commentSectionId, json_comments) {
    for (i = 0; i < json_comments.results.length; i++) {
        var comment = createComment(json_comments.results[i].id, json_comments.results[i].author,
                                    json_comments.results[i].update_date, json_comments.results[i].content,
                                    json_comments.results[i].author_username, json_comments.results[i].author_slug,
                                    json_comments.results[i].author_avatar, json_comments.results[i].points);

        var commentId = json_comments.results[i].id;
        $(commentSectionId).append(comment);

        for (j = 0; j < json_comments.results[i].replies.length; j++) {

            var reply = createReply(json_comments.results[i].replies[j].id,
                                    commentId,
                                    json_comments.results[i].replies[j].response_to,
                                    json_comments.results[i].replies[j].author,
                                    json_comments.results[i].replies[j].update_date,
                                    json_comments.results[i].replies[j].content,
                                    json_comments.results[i].replies[j].author_username,
                                    json_comments.results[i].replies[j].author_slug,
                                    json_comments.results[i].replies[j].author_avatar,
                                    json_comments.results[i].replies[j].points);

            var commentChain = $('#comment-' + commentId + ' #replies');
            commentChain.append(reply);

            return commentChain;
        };
    }
}

function createCommentSection(commentSectionId, json_comments) {
    for (i = 0; i < json_comments.results.length; i++) {
        var comment = createComment(json_comments.results[i].id,            json_comments.results[i].author,
                                    json_comments.results[i].update_date,   json_comments.results[i].content,
                                    json_comments.results[i].author_username, json_comments.results[i].author_slug,
                                    json_comments.results[i].author_avatar, json_comments.results[i].points);

        var commentId = json_comments.results[i].id;
        $(commentSectionId).append(comment);

        for (j = 0; j < json_comments.results[i].replies.length; j++) {

            var reply = createReply(json_comments.results[i].replies[j].id,
                                    commentId,
                                    json_comments.results[i].replies[j].response_to,
                                    json_comments.results[i].replies[j].author,
                                    json_comments.results[i].replies[j].update_date,
                                    json_comments.results[i].replies[j].content,
                                    json_comments.results[i].replies[j].author_username,
                                    json_comments.results[i].replies[j].author_slug,
                                    json_comments.results[i].replies[j].author_avatar,
                                    json_comments.results[i].replies[j].points);
            
            $('#comment-' + commentId + ' #replies').append(reply);
        };
    }
}

function createComment(id, author, date, content, author_username, author_slug, author_avatar, points) {
    points = points || 0;

    date = new Date(date)

    var formatted_date = dateFormat(date)
    var time_since_date = timeSince(date);

    var div_comment = $('<div />').addClass('container media col-md-12').attr('id', 'comment-' + id).attr("data-id", id);

    var div_avatar_container = $('<div />').addClass('col-md-1 avatar-container');
    var img_avatar = $('<a />').attr('href', '/perfil/' + author_slug).append(
        $('<img />').addClass('col-md-12 img-rounded media-object').attr('src', "/media/" + author_avatar).css("width", "80")
        );

    div_avatar_container.append(img_avatar);

    var div_info_container = $('<div />').addClass('col-md-11 info-container');
    var a_author = $('<a />').attr('href', '/perfil/' + author_slug).html("<b>" + author_username + "</b>");
    var span_author = $('<span />').addClass('col-md-12').append(a_author);
    var span_date = $('<span />').addClass('col-md-12 comment-date').html("há " + time_since_date).attr('title', formatted_date);
    var span_content = $('<span />').addClass('col-md-12 comment-content').html(content);

    div_info_container.append(span_author).append(span_date).append(span_content);

    var div_feedback_container = $('<div />').addClass('col-md-12 feedback-container');
    var span_points = $('<span />').addClass('col-md-1 comment-points').html(points).attr('id', 'points-' + id);
    var button_upvote = $('<button />').addClass('btn btn-default btn-xs glyphicon glyphicon-chevron-up');
    var button_downvote = $('<button />').addClass('btn btn-default btn-xs glyphicon glyphicon-chevron-down');

    var button_reply = $('<button />').addClass('btn btn-default btn-xs').html("Responder");
    var textarea_reply = $('<textarea />').addClass('').css('display', 'none');
    var button_send = $('<button />').addClass('btn btn-default btn-xs').css('display', 'none').html("Enviar");

    var hr = $('<div />').addClass('col-md-12').append($('<hr />'));

    div_feedback_container.append(span_points).append(button_upvote).append(button_downvote).append(" | ").append(button_reply)
                        .append(textarea_reply).append(button_send);

    var div_content_container = $('<div />').addClass('col-md-11 content-container').append(div_info_container)
                            .append(div_feedback_container);

    var div_replies = $('<div />').addClass('col-md-12').attr('id', 'replies');

    button_reply.click(function () {
        textarea_reply.css('display', '');
        button_send.css('display', '');
        button_reply.css('display', 'none');
    });

    button_upvote.click(function () {
        sendVote(id, "comment", 1);
    });

    button_downvote.click(function () {
        sendVote(id, "comment", -1);
    });

    button_send.click(function () {
        sendReply(id, null, textarea_reply.val(), sendReplyApiEndpoint, getCommentApiEndpoint);
    });

    div_comment.append(div_avatar_container).append(div_content_container).append(hr).append(div_replies);
    return div_comment;
}

function createReply(id, parentCommentId, parentReplyId, author, date, content, author_username, author_slug, author_avatar, points) {
    points = points || 0;

    date = new Date(date)

    var formatted_date = dateFormat(date)
    var time_since_date = timeSince(date);

    var div_reply = $('<div />').addClass('container media col-md-12 reply-content').attr('id', 'reply-' + id).attr("data-id", id);

    var div_avatar_container = $('<div />').addClass('col-md-1 avatar-container');
    var img_avatar = $('<a />').attr('href', '/perfil/' + author_slug).append(
        $('<img />').addClass('col-md-12 img-rounded media-object').attr('src', "/media/" + author_avatar).css("width", "80")
        );

    div_avatar_container.append(img_avatar);

    var div_info_container = $('<div />').addClass('col-md-11 info-container');
    var a_author = $('<a />').attr('href', '/perfil/' + author_slug).html("<b>" + author_username + "</b>");
    var span_author = $('<span />').addClass('col-md-12').append(a_author);
    var span_date = $('<span />').addClass('col-md-12 comment-date').html("há " + time_since_date).attr('title', formatted_date);
    var span_content = $('<span />').addClass('col-md-12 comment-content').html(content);

    div_info_container.append(span_author).append(span_date).append(span_content);

    var div_feedback_container = $('<div />').addClass('col-md-12 feedback-container');
    var span_points = $('<span />').addClass('col-md-1 comment-points').html(points).attr('id', 'points-' + id);
    var button_upvote = $('<button />').addClass('btn btn-default btn-xs glyphicon glyphicon-chevron-up');
    var button_downvote = $('<button />').addClass('btn btn-default btn-xs glyphicon glyphicon-chevron-down');

    var button_reply = $('<button />').addClass('btn btn-default btn-xs').html("Responder");
    var textarea_reply = $('<textarea />').addClass('form-control');
    var button_send = $('<button />').addClass('btn btn-primary  btn-xs').html("Enviar");
    var textarea_reply_div = $('<div />').addClass('textarea col-md-12').css('display', 'none')
        .append(textarea_reply).append("<br>").append(button_send);

    div_feedback_container.append(span_points).append(button_upvote).append(button_downvote).append(" | ").append(button_reply)
                        .append(textarea_reply_div);

    var div_content_container = $('<div />').addClass('col-md-11 content-container').append(div_info_container).append(div_feedback_container);

    var hr = $('<div />').addClass('col-md-12').append($('<hr />'));

    button_upvote.click(function () {
        sendVote(id, "reply", 1);
    });

    button_downvote.click(function () {
        sendVote(id, "reply", -1);
    });

    button_reply.click(function () {
        textarea_reply_div.css('display', '');
        button_send.css('display', '');
        button_reply.css('display', 'none');
    });

    button_send.click(function () {
        sendReply(parentCommentId, id, textarea_reply.val(), sendReplyApiEndpoint, getCommentApiEndpoint);
    });

    div_reply.append(div_avatar_container).append(div_content_container).append(hr);
    return div_reply;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var timeSince = function (date)
{
    var seconds = Math.floor((new Date() - date) / 1000);
    var intervalType;

    var interval = Math.floor(seconds / 31536000);

    if (interval >= 1)
        intervalType = 'ano';
    else
    {
        interval = Math.floor(seconds / 2592000);

        if (interval >= 1)
            intervalType = 'mês';
        else
        {
            interval = Math.floor(seconds / 86400);

            if (interval >= 1)
                intervalType = 'dia';
            else
            {
                interval = Math.floor(seconds / 3600);

                if (interval >= 1)
                    intervalType = "hora";
                else
                {
                    interval = Math.floor(seconds / 60);

                    if (interval >= 1)
                        intervalType = "minuto";
                    else
                    {
                        interval = seconds;
                        intervalType = "segundo";
                    }
                }
            }
        }
    }

    if (intervalType == "mês")
    {
        if (interval > 1 || interval === 0 && intervalType != "mês")
            intervalType += 's';
    }

    if (interval > 1 || interval === 0)
    {
        if (intervalType == "mês")
            intervalType = 'meses';
        else
            intervalType += 's';
    }

    return interval + ' ' + intervalType;
};

var dateFormat = function (date) {
    var new_date = date.toLocaleDateString('pt-br', {
        weekday: 'short',
        day: 'numeric',
        month: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        timeZoneName: 'short'
    }).split(' de ').join('/');

    new_date = new_date.charAt(0).toUpperCase() + new_date.slice(1);

    return new_date;
};