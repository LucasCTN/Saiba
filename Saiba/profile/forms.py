from django import forms
from django.forms import ModelForm
from django.db import models
from profile.models import Profile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username    = forms.CharField(max_length = 500)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))

class RegisterProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ "gender"]

class RegisterUserForm(ModelForm):
    email       = models.EmailField(max_length = 500, blank = False)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))

    class Meta:
        model = User
        fields = [ "username", "password", "email"]