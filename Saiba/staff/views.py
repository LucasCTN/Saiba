from django.shortcuts import render, redirect
from home.forms import PostForm
from entry.models import Entry

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
        return redirect('staff:create_post')

    args = {'form': text_form}

    return render(request, 'staff/create_post.html', args)