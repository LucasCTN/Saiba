from django.shortcuts import render
from django.utils.html import escape
from entry.models import Entry

def index(request):
    entries = Entry.objects.all()
    return render(request, escape('home/index.html'), {'entries': entries})