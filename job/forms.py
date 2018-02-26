from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from job.models import Application

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Required')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required')
    email = forms.EmailField(max_length=250, help_text='Required')

    #def __init__(self):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ApplicationForm(forms.ModelForm):
    phone_number = forms.IntegerField(max_value=99999999, min_value=10000000)
    text = forms.CharField(max_length=2000)

    class Meta:
        model = Application
        fields = ('phone_number', 'text')
