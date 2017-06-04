from django.shortcuts import render
from django.utils.html import escape

def index(request):
    return render(request, escape('forum/index.html'), {'testes': [1, 2, 3, 4, 5, 6]})