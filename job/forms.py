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


class ApplicationForm(forms.ModelForm):
    text = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(), help_text='Write your application here!' )

    class Meta:
        model = Application
        exclude = ['applicant', 'weight']
        fields = ('text', 'phone_number', 'trondheim')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['trondheim'].widget.attrs.update({'class': 'form-control'})