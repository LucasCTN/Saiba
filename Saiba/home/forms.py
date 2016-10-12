from django import forms
from django.forms import ModelForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import models
from .models import Post
from profile.models import Profile

class ProfileForm(forms.Form):
    username    = forms.CharField(max_length = 500)
    password    = forms.PasswordInput()

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [ "category", "title", "content", "hidden", "entry", "image", "video"]