from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.
def index(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)
    return render(request, 'profile/index.html', {"profile":profile})