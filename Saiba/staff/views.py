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

    if search_term == None:
        all_users = User.objects.order_by("-date_joined")
    else:
        all_users = User.objects.filter(username__contains=search_term).order_by("-date_joined")

    args = {'all_users': all_users}

    return render(request, 'staff/search_user.html', args)

def search_user_result(request):
    if not request.user.is_staff:
        return redirect('home:index')

    all_users = User.objects.order_by("-date_joined")

    args = {'all_users': all_users}

    return render(request, 'staff/search_user.html', args)