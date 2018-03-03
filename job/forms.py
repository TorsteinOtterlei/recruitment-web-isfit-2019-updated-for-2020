from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from job.models import Application
from .models import Job, Gang, Section
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Required')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required')
    email = forms.EmailField(max_length=250, help_text='Required')

    #def __init__(self):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.title)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['applicant', 'weight']
        fields = ('text', 'phone_number', 'trondheim')

