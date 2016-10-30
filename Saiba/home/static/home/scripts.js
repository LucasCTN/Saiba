function sendComment(formType, formSlug, formContent, sendCommentapiEndpoint, getCommentapiEndpoint) {
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
        url: sendCommentapiEndpoint,
        data: { type: formType, slug: formSlug, content: formContent },
        success: function (data) {
            updateCommentSection("#comment-section", getCommentapiEndpoint);
        }
    })
}

function updateCommentSection(commentSectionId, getCommentapiEndpoint) {
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
        url: getCommentapiEndpoint,
        data: $(this).serialize(),
        success: function (data) {
            createCommentSection(commentSectionId, data);
        }
    })
}


function createCommentSection(commentSectionId, json_comments) {
    $(commentSectionId).empty();
    for (i = 0; i < json_comments.results.length; i++) {
        var comment = createComment(json_comments.results[i].id, json_comments.results[i].author,
                                    json_comments.results[i].update_date, json_comments.results[i].content);

                
        $(commentSectionId).append(comment);

        for (j = 0; j < json_comments.results[i].replies.length; j++) {
            var reply = createReply(json_comments.results[i].replies[j].id,
                                    json_comments.results[i].replies[j].author, 
                                    json_comments.results[i].replies[j].update_date,
                                    json_comments.results[i].replies[j].content);   
                    
            $('#comment-' + (i + 1) + ' #replies').append(reply.cloneNode(true));
        };
    }
}

function createComment(id, author, date, content){
    var div_comment     = document.createElement('div');
    var span_author     = document.createElement('span');
    var span_date       = document.createElement('span');
    var span_content    = document.createElement('span');
    var div_replies     = document.createElement('div');

    div_comment.className   += "col-md-12";
    span_author.className   += "col-md-12";
    span_date.className     += "col-md-12";
    span_content.className  += "col-md-12";
    div_replies.className   += "col-md-12";

    div_comment.id          = "comment-" + id;
    div_replies.id          = "replies";

    span_author.innerHTML   = author
    span_date.innerHTML     = date
    span_content.innerHTML  = content

    div_comment.appendChild(span_author.cloneNode(true));
    div_comment.appendChild(span_date.cloneNode(true));
    div_comment.appendChild(span_content.cloneNode(true));
    div_comment.appendChild(div_replies.cloneNode(true));

    return div_comment;
}

function createReply(id, author, date, content) {
    var div_reply       = document.createElement('div');
    var span_author     = document.createElement('span');
    var span_date       = document.createElement('span');
    var span_content    = document.createElement('span');

    div_reply.className     += "col-md-12";
    span_author.className   += "col-md-12";
    span_date.className     += "col-md-12";
    span_content.className  += "col-md-12";

    div_reply.id          = "reply-" + id;

    span_author.innerHTML   = author;
    span_date.innerHTML     = date;
    span_content.innerHTML  = content;

    div_reply.appendChild(span_author.cloneNode(true));
    div_reply.appendChild(span_date.cloneNode(true));
    div_reply.appendChild(span_content.cloneNode(true));
            
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