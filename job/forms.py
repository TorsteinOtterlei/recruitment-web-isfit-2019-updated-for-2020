from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from job.models import Application#, Ranking
from django.forms import inlineformset_factory
from .models import Position, Gang, Section, Ranking
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

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = 'Your password cant be too similar to your other personal information. Your password must contain atleast 8 characters. Your password cant be a commonly used password and cant be entierly numeric.'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ApplicationForm(forms.ModelForm):
    text = forms.CharField(label="Why do you want to volunteer with ISFiT? (Remember to write a ranking list of your top 3 choices where nr. 1 is your top choice)", max_length=2000, required=True, widget=forms.Textarea())

    class Meta:
        model = Application#, Ranking
        exclude = ['applicant']
        fields = ('text', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})


class RankingForm(forms.ModelForm):
    first = Position.objects.get(id=1)
    second = Position.objects.get(id=1)
    third = Position.objects.get(id=1)

    class Meta:
        model = Ranking
        exclude = []
        fields = ('first', 'second', 'third')

    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs)


#RankFormSet = inlineformset_factory(Application, Ranking, fields=('rank',))
#rankForPosition = Ranking.objects.get(position=Ranking.position)
#formset = RankFormSet(instance=rankForPosition)
