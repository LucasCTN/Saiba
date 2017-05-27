from profile.models import Profile

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from entry.models import Entry, EntryRedirect
from home.forms import PostForm


# Create your views here.
def index(request):
    if not request.user.is_staff:
        return redirect('home:index')

    return render(request, 'staff/index.html', {'current_page': 'index'})

def create_post(request):
    if not request.user.is_staff:
        return redirect('home:index')

    text_form = PostForm(request.POST or None)

    text_form.fields['label'].widget.attrs['class'] = 'form-control form-label'
    text_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    text_form.fields['content'].widget.attrs['class'] = 'form-control form-content'
    text_form.fields['entry'].widget.attrs['class'] = 'form-control form-entry'
    text_form.fields['image'].widget.attrs['class'] = 'form-control form-image'
    text_form.fields['video'].widget.attrs['class'] = 'form-control form-video'

    text_form.fields['content'].widget.attrs['rows'] = '4'

    text_form = PostForm(request.POST or None)

    text_form.fields['label'].widget.attrs['class'] = 'form-control form-label'
    text_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    text_form.fields['content'].widget.attrs['class'] = 'form-control form-content'
    text_form.fields['entry'].widget.attrs['class'] = 'form-control form-entry'
    text_form.fields['image'].widget.attrs['class'] = 'form-control form-image'
    text_form.fields['video'].widget.attrs['class'] = 'form-control form-video'

    text_form.fields['content'].widget.attrs['rows'] = '4'

    if text_form.is_valid():
        post = text_form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('home:index')

    args = {'form': text_form, 'current_page': 'postagem'}

    return render(request, 'staff/create_post.html', args)

def search_user(request):
    if not request.user.is_staff:
        return redirect('home:index')

    can_promote_users = request.user.profile.HasPermission('promote_user') or False

    search_term = request.GET.get("q")
    banned_user_id = request.GET.get("banned_user")
    unbanned_user_id = request.GET.get("unbanned_user")
    promoted_user_mod_id = request.GET.get("promoted_user_mod")
    demoted_user_mod_id = request.GET.get("demoted_user_mod")
    promoted_user_admin_id = request.GET.get("promoted_user_admin")
    demoted_user_admin_id = request.GET.get("demoted_user_admin")

    if search_term is None:
        all_users = User.objects.order_by("-date_joined")
    else:
        all_users = User.objects.filter(username__contains=search_term).order_by("-date_joined")

    # Banning an normal user
    if banned_user_id != None:
        banned_user = User.objects.filter(id=banned_user_id).first()
        if banned_user.is_staff and request.user.profile.HasPermission('ban_staff_user') or not banned_user.is_staff and request.user.profile.HasPermission('ban_normal_user'):
            banned_user.is_active = False
            banned_user.save()

    # Banning an staff user
    if unbanned_user_id != None:
        unbanned_user = User.objects.filter(id=unbanned_user_id).first()
        if not unbanned_user.is_active and unbanned_user.is_staff and request.user.profile.HasPermission('ban_staff_user') or not unbanned_user.is_staff and request.user.profile.HasPermission('ban_normal_user'):
            unbanned_user.is_active = True
            unbanned_user.save()

    # Promoting a user to moderator
    if promoted_user_mod_id != None:
        promoted_user = User.objects.filter(id=promoted_user_mod_id).first()
        if can_promote_users:
            promoted_user.profile.AddGroup('mod')

    # Demote a user to moderator
    if demoted_user_mod_id != None:
        demoted_user = User.objects.filter(id=demoted_user_mod_id).first()
        if can_promote_users:
            demoted_user.profile.RemoveGroup('mod')

    # Promoting a user to administrator
    if promoted_user_admin_id != None:
        promoted_user = User.objects.filter(id=promoted_user_admin_id).first()
        if can_promote_users:
            promoted_user.profile.AddGroup('admin')

    ban_normal_user = request.user.profile.HasPermission('ban_normal_user') or False
    ban_staff_user = request.user.profile.HasPermission('ban_staff_user') or False

    args = {'all_users': all_users, 'ban_normal_user': ban_normal_user,
            'ban_staff_user': ban_staff_user, 'current_page': 'usuarios', 'can_promote_users':True}

    return render(request, 'staff/search_user.html', args)

@staff_member_required
def entry_redirect(request):
    redirect_slug = request.POST.get("redirect_slug")
    entry_slug = request.POST.get("entry_slug")

    redirect = None

    if redirect_slug and entry_slug:
        entry = get_object_or_404(Entry, slug=entry_slug)
        redirect = EntryRedirect.objects.create(entry=entry, slug=redirect_slug)

    context = {'redirect': redirect, 'current_page': 'redirecionar'}
    return render(request, 'staff/entry_redirect.html', context)
