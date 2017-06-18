from django import forms
from django.forms import ModelForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import models
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [ "label", "title", "content", "hidden", "entry", "image", "video", "fixed"]

        widgets = {
          'label': forms.Select(attrs={'class': 'form-control form-label'}),
          'title': forms.TextInput(attrs={'class': 'form-control form-title'}),
          'content': forms.Textarea(attrs={'class': 'form-control form-content', 'rows': '4'}),
          'entry': forms.Select(attrs={'class': 'form-control form-entry'}),
          'image': forms.Select(attrs={'class': 'form-control form-image'}),
          'video': forms.Select(attrs={'class': 'form-control form-video'}),
        }