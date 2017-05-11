from django.shortcuts import render, redirect
from home.forms import PostForm
from entry.models import Entry
from profile.models import Profile
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if not request.user.is_staff:
        return redirect('home:index')

    return render(request, 'staff/index.html')

def create_post(request):
    if not request.user.is_staff:
        return redirect('home:index')

    text_form = PostForm(request.POST or None)

    #text_form.fields['label'].widget.attrs['style'] = 'color:red;'
    text_form.fields['label'].widget.attrs['class'] = 'form-control form-label'
    text_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    text_form.fields['content'].widget.attrs['class'] = 'form-control form-content'
    text_form.fields['entry'].widget.attrs['class'] = 'form-control form-entry'
    text_form.fields['image'].widget.attrs['class'] = 'form-control form-image'
    text_form.fields['video'].widget.attrs['class'] = 'form-control form-video'

    text_form.fields['content'].widget.attrs['rows'] = '4'

    text_form = PostForm(request.POST or None)

    #text_form.fields['label'].widget.attrs['style'] = 'color:red;'
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

    args = {'form': text_form}

    return render(request, 'staff/create_post.html', args)

def search_user(request):
    if not request.user.is_staff:
        return redirect('home:index')

    search_term = request.GET.get("q")
    banned_user_id = request.GET.get("banned_user")
    unbanned_user_id = request.GET.get("unbanned_user")

    if search_term == None:
        all_users = User.objects.order_by("-date_joined")
    else:
        all_users = User.objects.filter(username__contains=search_term).order_by("-date_joined")

    if banned_user_id != None:
        banned_user = User.objects.filter(id=banned_user_id).first()
        if banned_user.is_staff and request.user.profile.HasPermission('ban_staff_user') or not banned_user.is_staff and request.user.profile.HasPermission('ban_normal_user'): 
            banned_user.is_active = False
            banned_user.save()
            print banned_user.username + " foi banido!"

    if unbanned_user_id != None:
        print "oi"
        unbanned_user = User.objects.filter(id=unbanned_user_id).first()
        if not unbanned_user.is_active and unbanned_user.is_staff and request.user.profile.HasPermission('ban_staff_user') or not unbanned_user.is_staff and request.user.profile.HasPermission('ban_normal_user'): 
            unbanned_user.is_active = True
            unbanned_user.save()
            print unbanned_user.username + " foi desbanido!"
    
    ban_normal_user = request.user.profile.HasPermission('ban_normal_user') or False
    ban_staff_user = request.user.profile.HasPermission('ban_staff_user') or False

    args = {'all_users': all_users, 'ban_normal_user': ban_normal_user, 'ban_staff_user': ban_staff_user}

    return render(request, 'staff/search_user.html', args)

def search_user_result(request):
    if not request.user.is_staff:
        return redirect('home:index')

    all_users = User.objects.order_by("-date_joined")
    ban_normal_user = request.user.profile.HasPermission('ban_normal_user') or False
    ban_staff_user = request.user.profile.HasPermission('ban_staff_user') or False

    args = {'all_users': all_users, 'ban_normal_user': ban_normal_user, 'ban_staff_user': ban_staff_user}

    return render(request, 'staff/search_user.html', args)