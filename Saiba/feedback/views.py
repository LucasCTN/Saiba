from django.shortcuts import render
import feedback.services

def comment_page(request):
    id   = request.GET.get('id') or ""
    type = request.GET.get('type') or ""
    reply_limit = request.GET.get('reply_limit') or 5

    comments = feedback.services.get_target_parent_comments(id, type)

    args = { 'comments' : comments }

    return render(request, 'feedback/comment_page.html', args)