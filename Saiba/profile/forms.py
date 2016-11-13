from django import forms
from django.forms import ModelForm
from django.db import models
from profile.models import Profile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    user    = forms.CharField(max_length = 500)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))

'''class RegisterForm(forms.Form):
    username    = forms.CharField(max_length = 500)
    password    = forms.CharField(widget=forms.PasswordInput(render_value = True))
    email       = forms.CharField(max_length = 500)
    pronoun     = forms.ChoiceField(choices = (('Ele', 'Ele'), ('Ela', 'Ela'), ('Ele(a)', 'Ele(a)')))'''

class RegisterProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ "gender"]

class RegisterUserForm(ModelForm):
    email = models.EmailField(max_length = 500, blank = False)

    class Meta:
        model = User
        fields = [ "username", "password", "email"]