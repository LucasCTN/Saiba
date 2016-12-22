from django.shortcuts import render, redirect
from home.forms import PostForm
from entry.models import Entry

# Create your views here.
def index(request):

    if not request.user.is_staff:
        return redirect('home:index')

    return render(request, 'staff/index.html')