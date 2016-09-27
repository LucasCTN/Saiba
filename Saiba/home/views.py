from django.shortcuts import render
from django.utils.html import escape

def index(request):
    testes = [1, 2, 3, 4, 5, 6]
    return render(request, escape('home/index.html'), {'testes': testes})