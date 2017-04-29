from django.shortcuts import render
import feedback.services

def comment_page(request):
    id   = request.GET.get('id') or ""
    type = request.GET.get('type') or ""
    child_limit = request.GET.get('child_limit') or 5
    page = int(request.GET.get('page')) or 1

    comments_limit = 10

    comments = feedback.services.get_target_comment_page(id, type, page, comments_limit)
    pages_total = feedback.services.get_target_page_count(id, type, comments_limit)
    pages_total = int(pages_total)

    args = { 'comments' : comments, 'pages_total': range(1, pages_total + 1), 'current_page': page }

    return render(request, 'feedback/comment_page.html', args)