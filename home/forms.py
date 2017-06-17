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