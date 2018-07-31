from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.forms import inlineformset_factory
from .models import *
#from django.forms.widgets import CheckboxSelectMultiple
#from django.forms.models import ModelMultipleChoiceField

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250, required=True, help_text='Required')
    first_name = forms.CharField(max_length=50, required=True, help_text='Required')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required')
    phone_number = models.CharField(max_length=12)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        #self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = 'Your password cant be too similar to your other personal information. Your password must contain atleast 8 characters. Your password cant be a commonly used password and cant be entierly numeric.'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
