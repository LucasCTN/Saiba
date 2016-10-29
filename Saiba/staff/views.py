from django.shortcuts import render, redirect
from home.forms import PostForm
from entry.models import Entry

# Create your views here.
def index(request):
    entries = Entry.objects.all()

    text_form = PostForm(request.POST or None)

    if text_form.is_valid():
        post = text_form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('home:index')

    args = {'entries': entries,
            'form': text_form}

    return render(request, 'staff/index.html', args)