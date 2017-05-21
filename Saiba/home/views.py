import urllib2, urllib, json
from rest_framework.reverse import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.contrib.auth.models import Permission, User
from .models import Post, Label, Tag
from .forms import PostForm
from profile.forms import LoginForm, RegisterProfileForm, RegisterUserForm
from entry.models import Entry, Revision
from gallery.models import Image, Video
from profile.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from Saiba import utils
import copy
from api.views import TrendingDetail

def index(request):
    entries = Entry.objects.all()

    posts = Post.objects.all().order_by('-date')
    fixed_posts = Post.objects.filter(fixed=True).order_by('-date')
    normal_posts = Post.objects.filter(fixed=False).order_by('-date')

    args = {'entries': entries,
            'posts': posts,
            'fixed_posts': fixed_posts,
            'normal_posts': normal_posts}

    return render(request, 'home/index.html', args)

def user_login(request):
    errors_list = []

    if request.user.is_authenticated():
        return redirect('home:index')
    else:
        username = password = ''
        
        profile_form = LoginForm(request.POST or None)

        if profile_form.is_valid():
            if initialize_authentification(request):
                return redirect('home:index')
            else:                
                if len(User.objects.filter(username=request.POST['username'])) <= 0:
                    errors_list.append("Este nome de usuario nao esta registrado no sistema.")
                else:
                    errors_list.append("A senha digitada esta incorreta.")

        profile_form.fields['username'].widget.attrs['class'] = 'form-control form-username'
        profile_form.fields['password'].widget.attrs['class'] = 'form-control form-password'

        args = {'form': profile_form,
                'errors_list': errors_list}

        return render(request, 'home/login.html', args)

def initialize_authentification(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return True
        else:
            return False

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)

    return redirect('home:index')

def user_register(request):
    if request.user.is_authenticated():
        return redirect('home:index')
    else:
        register_profile_form = RegisterProfileForm(request.POST or None)
        register_user_form = RegisterUserForm(request.POST or None)
        register_user_form.fields['email'].required = True
        
        custom_error = []
        original_errors = {}
        original_errors["Enter a valid email address."] = "Digite um endereco de email valido."
        original_errors["A user with that username already exists."] = "Ja existe um usuario com este nome."

        if request.POST:
            for x in register_user_form:
                for error in x.errors:
                    custom_error.append(original_errors[str(error)])

            if(User.objects.filter(email=request.POST['email'])):
                custom_error.append("Esse email ja foi registrado.")
            else:
                if request.POST['repeat_password'] != request.POST['password']:
                    custom_error.append("As senhas nao sao iguais.")
                else:
                    if register_user_form.is_valid() and register_profile_form.is_valid():                
                        user = register_user_form.save()
                        user.set_password(user.password)
                        user.save()

                        profile = register_profile_form.save(commit=False)
                        profile.user = user
                        profile.save()

                        if initialize_authentification(request):
                            return redirect('home:index')

        register_user_form.fields['username'].widget.attrs['class'] = 'form-control form-username'
        register_user_form.fields['password'].widget.attrs['class'] = 'form-control form-password'
        register_user_form.fields['email'].widget.attrs['class'] = 'form-control form-email'
        register_profile_form.fields['gender'].widget.attrs['class'] = 'form-control form-gender'
    
        args = {'user_form': register_user_form,
                'profile_form': register_profile_form,
                'custom_error': custom_error}
    
        return render(request, 'home/register.html', args)

def page_search(request):
    query = request.GET.get('q')
    type = request.GET.get('tipo')
    order_by = request.GET.get('ordenar_por')
    entry_slug = request.GET.get('entrada')

    if query == None:
        query = ''

    if type == None:
        type = 'entrada'

    if order_by == None:
        order_by = 'novo'

    if entry_slug == None:
        entry_slug = ''

    if(type == 'entrada' and entry_slug != ''):
        search_result = None
    else:
        if(type == 'entrada'):
            search_result = Entry.objects.filter(hidden=False)
        elif(type == 'imagem'):
            search_result = Image.objects.filter(hidden=False)
        else:
            search_result = Video.objects.filter(hidden=False)

        if(query != ''):
            search_result = search_result.filter(Q(title__contains=query) | Q(tags__label__contains=query)).distinct()

        if(entry_slug != '' and type != 'entrada'):
            entrada = Entry.objects.filter(slug=entry_slug, hidden=False).first()
            search_result = search_result.filter(entry=entrada)

        if(order_by == 'novo'):
            search_result = search_result.order_by('-id')
        elif(order_by == 'antigo'):
            search_result = search_result.order_by('id')

        for result in search_result:
            if(type == 'entrada'):
                result.href = "/entrada/" + result.slug
                result.src = "/media/" + str(result.icon)
            elif(type == 'imagem'):
                result.href = "/galeria/imagem/" + str(result.id)
                result.src = "/media/" + str(result.file)
            else:
                result.href = "/galeria/video/" + str(result.id)
                result.src = "https://img.youtube.com/vi/" + result.link + "/mqdefault.jpg"
    
    args = {'search_result' : search_result,
            'query' : query,
            'type' : type,
            'order_by' : order_by,
            'entry' : entry_slug}

    return render(request, 'home/search.html', args)

def navbar_search(request):
    if request.GET:
        search_text = request.GET.get('q')
    else:
        search_text = ''

    entries = Entry.objects.all()

    if search_text != '':
        search_result = Entry.objects.filter(title__contains=search_text, hidden=False)[:5]
    else:
        search_result = None

    args = {'entries' : entries,
            'navbar_search_result' : search_result}

    return render(request, 'home/navbar_search.html', args)

def search_entry(request):
    if request.GET:
        search_text = request.GET.get('q')
    else:
        search_text = ''

    entries = Entry.objects.all()

    if search_text != '':
        search_result = Entry.objects.filter(title__contains=search_text, hidden=False)[:5]
    else:
        search_result = None

    args = {'entries' : entries,
            'entry_search_result' : search_result}

    return render(request, 'home/search_entry.html', args)

def search_tag(request):
    if request.GET:
        search_text = request.GET.get('q')
    else:
        search_text = ''

    if search_text != '':
        tag_search_result = Tag.objects.filter(label__contains=search_text, hidden=False)[:5]
    else:
        tag_search_result = None

    args = { 'tag_search_result' : tag_search_result }

    return render(request, 'home/search_tag.html', args)

def trending_page(request):
    new_request = copy.copy(request)
    new_request.method = "GET" #This is horrible

    trending_entries = TrendingDetail.as_view()(new_request, "entry").data
    result = trending_entries[:5]

    return render(request, 'home/trending.html', {'trending_entries': result})

def popular_images(request):
    new_request = copy.copy(request)
    new_request.method = "GET" #This is horrible

    trending_galleries = TrendingDetail.as_view()(new_request, "gallery").data
    result = trending_galleries[:5]
    return render(request, 'home/popular_galleries.html', {'galleries': result})

def trending_list(request):
    new_request = copy.copy(request)
    trending_type = request.GET.get('type') or "image"
    trending_list = TrendingDetail.as_view()(new_request, trending_type).data

    return render(request, 'home/trending_list.html', {'trending_list': trending_list})