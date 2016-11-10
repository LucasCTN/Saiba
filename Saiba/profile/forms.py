from django import forms
from django.forms import ModelForm
from django.db import models
from profile.models import Profile

class LoginForm(forms.Form):
    username    = forms.CharField(max_length = 500)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))

class RegisterForm(forms.Form):
    username    = forms.CharField(max_length = 500)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))
    email       = forms.CharField(max_length = 500)