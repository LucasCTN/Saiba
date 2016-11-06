var API = function (getCommentEndpoint, postCommentEndpoint, sendReplyEndpoint, voteEndpoint) {
    this.postCommentEndpoint = postCommentEndpoint;
    this.getCommentEndpoint = getCommentEndpoint;
    this.sendReplyEndpoint = sendReplyEndpoint;
    this.voteEndpoint = voteEndpoint;
    
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie("csrftoken");
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

API.prototype.getCommentPage = function () {
    return $.ajax({
        type: "GET",
        url: this.getCommentEndpoint,
        context: this
    })
};

API.prototype.postGenericComment = function (id, slug, type, content) {
    return $.ajax({
        type: "POST",
        url: this.postCommentEndpoint,
        context: this,
        data: { id: id, slug: slug, type: type, content: content }
    })
};

API.prototype.postEntryComment = function (slug, content) {
    return this.postGenericComment(null, slug, "entry", content);
};

API.prototype.postImageComment = function (id, content) {
    return this.postGenericComment(id, null, "image", content);
};

API.prototype.postVideoComment = function (id, content) {
    return this.postGenericComment(id, null, "video", content);
};

API.prototype.postReply = function (commentId, responseToId, content) {
    return $.ajax({
        type: "POST",
        url: this.sendReplyEndpoint,
        context: this,
        data: { comment: commentId, content: content, response_to: responseToId }
    })
};

API.prototype.postReply = function (commentId, responseToId, content) {
    return $.ajax({
        type: "POST",
        url: this.sendReplyEndpoint,
        context: this,
        data: { comment: commentId, content: content, response_to: responseToId }
    })
};

API.prototype.getVotes = function (contentId, contentType) {
    return $.ajax({
        type: "GET",
        url: this.voteEndpoint,
        data: 'id=' + contentId + '&type=' + contentType,
        context: this
    })
};

API.prototype.postVote = function (contentId, contentType, direction) {
    return $.ajax({
        type: "POST",
        url: this.sendReplyEndpoint,
        context: this,
        data: { id: contentId, type: contentType, direction: direction }
    })
};