from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
import feedback.services
from .models import Comment

def comment_page(request):
    model_id = request.GET.get('id') or ""
    model_type = request.GET.get('type') or ""
    child_limit = request.GET.get('child_limit') or 5
    chain = request.GET.get('chain') or ""
    page = int(request.GET.get('page')) or 1
    hide_top_comments = request.GET.get('hide_top_comments') or False

    comments_limit = 10

    comments = feedback.services.get_target_comment_page(model_id, model_type, page, comments_limit)
    pages_total = feedback.services.get_target_page_count(model_id, model_type, comments_limit)
    pages_total = int(pages_total)

    user_can_delete = request.user.profile.HasPermission('delete_comment')

    model_type = feedback.services.convert_type(model_type)
    top_comments = Comment.objects.filter(target_content_type=model_type, target_id=model_id, is_deleted=False)
    top_comments = top_comments.order_by('-points')[:2]

    args = {'comments' : comments, 'pages_total': range(1, pages_total + 1), 'current_page': page,
            'chain': chain, 'child_limit': child_limit, 'user_can_delete': user_can_delete, 'top_comments':top_comments, 'hide_top_comments':hide_top_comments}

    return render(request, 'feedback/comment_page.html', args)
