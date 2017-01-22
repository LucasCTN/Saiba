from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.contrib.auth.models import Permission, User
from .models import Post, Label
from .forms import PostForm
from profile.forms import LoginForm, RegisterProfileForm, RegisterUserForm
from entry.models import Entry, Revision
from gallery.models import Image, Video
from profile.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

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

def navbar_search(request):
    query = request.GET.get('q')
    type = request.GET.get('type')
    order_by = request.GET.get('order_by')
    
    entries = Entry.objects.all()

    if query == None:
        query = ''

    if type == None:
        type = 'entry'

    if order_by == None:
        order_by = 'newer'
    
    search_result = None;
    
    if(type == 'entry'):
        search_result = Entry.objects.filter(Q(title__contains=query, hidden=False) | Q(tags__label__contains=query)).distinct()
    elif(type == 'image'):
        search_result = Image.objects.filter(Q(title__contains=query, hidden=False) | Q(tags__label__contains=query)).distinct()
    elif(type == 'video'):
        search_result = Video.objects.filter(Q(title__contains=query, hidden=False) | Q(tags__label__contains=query)).distinct()

    if(order_by == 'newer'):
        search_result = search_result.order_by('-id')
    elif(order_by == 'older'):
        search_result = search_result.order_by('id')
    
    args = {'entries' : entries,
            'search_result' : search_result,
            'query' : query,
            'type' : type,
            'order_by' : order_by}

    return render(request, 'home/search.html', args)

def search_results(request):
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

    return render(request, 'home/search_entry.html', args)