from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.contrib.auth.models import Permission, User
from .models import Post, Label
from .forms import PostForm
from profile.forms import LoginForm
from entry.models import Entry
from gallery.models import Image, Video
from profile.models import Profile
from django.contrib.auth import authenticate, login, logout

def index(request):
    entries = Entry.objects.all()

    posts = Post.objects.all().order_by('-date')
    fixed_posts = Post.objects.filter(fixed=True).order_by('-date')
    normal_posts = Post.objects.filter(fixed=False).order_by('-date')

    text_form = PostForm(request.POST or None)
    modify_form(text_form)

    if text_form.is_valid():
        post = text_form.save(commit=False)
        post.author = request.user
        
        text_label = Label.objects.filter(name="Texto")[0]
        entry_label = Label.objects.filter(name="Meme")[0]
        imagem_label = Label.objects.filter(name="Imagem")[0]
        video_label = Label.objects.filter(name="Video")[0]

        if post.entry == None:
            if post.video == None:
                if post.image == None:
                    post.label = text_label
                else:
                    post.label = imagem_label
            else:
                post.label = video_label
        else:
            post.label = entry_label

        post.save()
        return redirect('home:index')

    args = {'entries': entries,
            'posts': posts,
            'fixed_posts': fixed_posts,
            'normal_posts': normal_posts,
            'form': text_form}

    return render(request, 'home/index.html', args)

def modify_form(form):
    #form.fields['label'].widget.attrs['style'] = 'color:red;'
    form.fields['label'].widget.attrs['class'] = 'form-control form-label'
    form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    form.fields['content'].widget.attrs['class'] = 'form-control form-content'
    form.fields['entry'].widget.attrs['class'] = 'form-control form-entry'
    form.fields['image'].widget.attrs['class'] = 'form-control form-image'
    form.fields['video'].widget.attrs['class'] = 'form-control form-video'

    form.fields['content'].widget.attrs['rows'] = '4'

def user_login(request):
    username = password = ''

    profile_form = LoginForm(request.POST or None)
    login_error = False

    if profile_form.is_valid():
        print "teste"
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home:index')
            else:
                login_error = True

    args = {'form': profile_form,
            'error': login_error}

    return render(request, 'home/login.html', args)

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)

    return redirect('home:index')

def user_register(request):
    if request.user.is_authenticated():
        logout(request)

    return render(request, 'home/register.html')