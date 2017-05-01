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

    this.sendComment = function (formId, formType, formContent, parent, reply_to, sendCommentApiEndpoint) {
        return $.ajax({
            type: "POST",
            url: sendCommentApiEndpoint,
            data: { id: formId, type: formType, content: formContent, parent: parent, reply_to: reply_to },
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

    this.markComment = function (id, is_deleted, endpoint) {
        return $.ajax({
            type: "PATCH",
            url: endpoint,
            data: { id: id, is_deleted: is_deleted },
            success: function (data) {
            }
        });
    }

    this.trending = function (url, callback) {
        return $.ajax({
            type: "PATCH",
            url: url,
            success: function (data) {
                if (callback)
                {
                    callback(data);
                }
            }
        });
    }
}

function CommentSection(section_id, user_slug) {
    var api = new API();
    var id = "#" + section_id;
    var current_page = 1;
    var chain = "";

    var comment_page_endpoint = commentPage;
    var comment_section = this;

    this.loadCommentPage = function (callback) {
        var comment_section = this;

        api.getCommentPage(comment_page_endpoint + "&page=" + current_page + "&chain=" + chain).done(function (data) {
            $(id).empty().append(data);

            $(".comment-reply").click(function () {
                $(this).css('display', 'none');
                $(this).siblings('.replybox').css('display', '');
                $(this).siblings('.replybox-send').css('display', '');
            });

            $(".upvote").click(function () {
                var comment_id = $(this).parents(".comment").attr("data-id");
                api.sendVote(comment_id, "comment", 1, voteApiEndpoint).done(function (data) {
                    comment_section.loadCommentPage();
                    comment_section.scrollToComment(comment_id);
                })
            }); 

            $(".downvote").click(function () {
                var comment_id = $(this).parents(".comment").attr("data-id");
                api.sendVote(comment_id, "comment", -1, voteApiEndpoint).done(function (data) {
                    comment_section.loadCommentPage();
                    comment_section.scrollToComment(comment_id);
                })
            });

            $(".replybox-send").click(function () {
                $(this).css('display', 'none');
                $(this).siblings('.replybox').css('display', 'none');
                $(this).siblings('.comment-reply').css('display', '');

                var replybox_content = $(this).siblings(".replybox").val();
                var parent = $(this).parents(".comment-chain").attr("data-id");
                var reply_to = $(this).parents(".comment").attr("data-id");

                api.sendComment(contentId, contentType, replybox_content, parent, reply_to, sendCommentApiEndpoint).done(function (data) {                    
                        var comment_id = data.id;
                        comment_section.loadCommentPage(function(){
                        comment_section.scrollToComment(comment_id);
                    });
                })
            });

            $(".comment-delete").click(function () {
                var comment_id = $(this).parents(".comment").attr("data-id");
                api.markComment(comment_id, true, sendCommentApiEndpoint).done(function () {
                    $(this).parents(".comment").remove();
                    comment_section.loadCommentPage(function(){
                        comment_section.scrollToComment(comment_id);
                    });
                })
                
            });

            $(".change-page").click(function () {
                current_page = $(this).attr("data-id");
                $("#comment-section").empty();
                comment_section.loadCommentPage();
            });

            $(".open-thread").click(function () {
                var comment_id = $(this).parents(".comment-chain").attr("data-id");
                chain = comment_id.toString();
                comment_section.loadCommentPage(function(){
                    comment_section.scrollToComment(comment_id);
                });
            });

            $(".close-thread").click(function () {
                chain = "";
                comment_section.loadCommentPage(function(){
                    comment_section.scrollToComment(comment_id);
                });
            });

            if (callback){
                callback();
            }
        });

         $('html, body').animate({
            scrollTop: $("#comment-section").offset().top
        }, 1);
    }

    this.scrollToComment = function (id) {
        var div_id = "#comment-" + id;

        $('html, body').animate({
            scrollTop: $(div_id).offset().top
        }, 3);
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