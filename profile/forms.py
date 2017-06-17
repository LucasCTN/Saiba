from django import forms
from django.forms import ModelForm
from django.db import models
from profile.models import Profile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username    = forms.CharField(max_length = 500)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))

class RegisterProfileForm(ModelForm):
    '''Form for registering, with Profile-specific fields.'''
    class Meta:
        model = Profile
        fields = ["gender"]

class RegisterUserForm(ModelForm):
    '''Form for registering, with User-specific fields.'''
    username = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-username'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control form-password'}))
    email = forms.EmailField(max_length=500, widget=forms.EmailInput(attrs={'class': 'form-control form-email'}))

    class Meta:
        model = User
        fields = ["username", "password", "email"]

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "gender", "location", "about"]
