function API() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    this.getCommentPage = function (endpoint) {
        return $.ajax({
            type: "GET",
            url: endpoint,
            data: "",
            cache: false,
            success: function (data) {
            }
        });
    }

    this.sendComment = function (formId, formType, formSlug, formContent, sendCommentApiEndpoint) {
        return $.ajax({
            type: "POST",
            url: sendCommentApiEndpoint,
            data: { type: formType, slug: formSlug, content: formContent, id: formId },
            success: function (data) {
            }
        });
    }

    this.sendReply = function (parentCommentId, parentReplyId, formContent, endpoint) {
        return $.ajax({
            type: "POST",
            url: endpoint,
            data: { comment: parentCommentId, content: formContent, response_to: parentReplyId },
            success: function (data) {
            }
        });
    }

    this.sendVote = function (contentId, type, direction, endpoint) {
        return $.ajax({
            type: "POST",
            url: endpoint,
            data: { id: contentId, type: type, direction: direction },
            success: function (data) {                
            }
        });
    }    
}

function CommentSection(section_id, api_comment_page, api_send_vote) {
    var api = new API();
    var id = "#" + section_id;

    var comment_page_endpoint = api_comment_page;
    var next_page = null;
    var loadedPages = 0;

    var comment_section = this;

    this.createComment = function createComment(type, data) {
        var div_id = "";
        if (type == "comment")
            div_id = "comment-" + data.id;
        else
            div_id = "reply-" + data.id;

        var div_comment = $('<div />').addClass(type + ' container media col-md-12').attr("data-id", data.id).attr("id", div_id);

        var div_avatar_container = $('<div />').addClass('col-md-1 avatar-container');
        var img_avatar = $('<a />').attr('href', '/perfil/' + data.author_slug).append(
            $('<img />').addClass('col-md-12 img-rounded media-object').attr('src', "/media/" + data.author_avatar).css("width", "80")
            );

        div_avatar_container.append(img_avatar);

        var div_info_container = $('<div />').addClass('col-md-11 info-container');
        var a_author = $('<a />').attr('href', '/perfil/' + data.author_slug).html("<b>" + data.author_username + "</b>");
        var span_author = $('<span />').addClass('col-md-12').append(a_author);
        var span_date = $('<span />').addClass('col-md-12 comment-date').html(GetDateText(data.creation_date)).attr('title', dateFormat(data.creation_date));
        var span_content = $('<span />').addClass('col-md-12 comment-content').html(data.content);

        div_info_container.append(span_author).append(span_date).append(span_content);

        var div_feedback_container = $('<div />').addClass('col-md-12 feedback-container');
        var span_points = $('<span />').addClass('col-md-1 comment-points').html(data.points || 0);
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

        var div_replies = $('<div />').addClass('replies col-md-12');

        button_reply.click(function () {
            textarea_reply.css('display', '');
            button_send.css('display', '');
            button_reply.css('display', 'none');
        });

        button_upvote.click(function () {
            api.sendVote(data.id, type, 1, voteApiEndpoint).done(function (data) {
                comment_section.loadCommentPage();
                comment_section.scrollToComment(div_id);
            })
        });

        button_downvote.click(function () {
            api.sendVote(data.id, type, -1, voteApiEndpoint).done(function (data) {
                comment_section.loadCommentPage();
                comment_section.scrollToComment(div_id);
            })
        });

        button_send.click(function () {
            api.sendReply(data.id, null, textarea_reply.val(), sendReplyApiEndpoint).done(function (reply_data) {
                //comment_section.loadCommentPage();
                var reply = comment_section.createComment("reply", reply_data);
                $("#comment-" + data.id + " .replies").append(reply);
                comment_section.scrollToComment("reply-" + reply_data.id);

                textarea_reply.css('display', 'none');
                button_send.css('display', 'none');
                button_reply.css('display', '');
            })            
        });

        div_comment.append(div_avatar_container).append(div_content_container).append(hr);

        if (type == "comment")
            div_comment.append(div_replies);
        return div_comment;
    }

    this.createCommentPage = function (data) {
        var comment_page = [];

        for (i = 0; i < data.results.length; i++) {
            var comment = this.createComment("comment", data.results[i]);
            comment_page.push(comment);

            for (j = 0; j < data.results[i].replies.length; j++) {
                var reply = this.createComment("reply", data.results[i].replies[j]);
                comment.find('.replies').append(reply);
            }
        }

        return comment_page;
    }

    this.loadCommentPage = function (pages, callback) {
        pages = pages || 0;
        var comment_section = this;
        loadedPages += 1;

        api.getCommentPage(comment_page_endpoint).done(function (data) {
            var comments = comment_section.createCommentPage(data);
            next_page = data.next;
            $(id).empty().append(comments);

            if (callback){
                callback();
            }
        });
    }

    this.appendNextCommentPage = function () {
        if (next_page != null) {
            var comment_section = this;
            loadedPages += 1;

            api.getCommentPage(next_page).done(function (data) {
                var comments = comment_section.createCommentPage(data);
                next_page = data.next;
                $(id).append(comments);
            });
        }
    }

    this.scrollToComment = function (id) {
        var div_id = "#" + id;
        console.log(div_id);

        $('html, body').animate({
            scrollTop: $(div_id).offset().top
        }, 1500);
    }
}

var GetDateText = function (raw_date) {
    var date = new Date(raw_date);
    var seconds = Math.floor((new Date() - date) / 1000);
    var intervalType;

    var interval = Math.floor(seconds / 31536000);

    if (interval >= 1)
        intervalType = 'ano';
    else {
        interval = Math.floor(seconds / 2592000);

        if (interval >= 1)
            intervalType = 'mês';
        else {
            interval = Math.floor(seconds / 86400);

            if (interval >= 1)
                intervalType = 'dia';
            else {
                interval = Math.floor(seconds / 3600);

                if (interval >= 1)
                    intervalType = "hora";
                else {
                    interval = Math.floor(seconds / 60);

                    if (interval >= 1)
                        intervalType = "minuto";
                    else {
                        interval = seconds;
                        intervalType = "segundo";
                    }
                }
            }
        }
    }

    if (intervalType == "mês") {
        if (interval > 1 || interval === 0 && intervalType != "mês")
            intervalType += 's';
    }

    if (interval > 1 || interval === 0) {
        if (intervalType == "mês")
            intervalType = 'meses';
        else
            intervalType += 's';
    }

    return interval + ' ' + intervalType + ' atrás';
};

var dateFormat = function (date_raw) {
    var date = new Date(date_raw);
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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