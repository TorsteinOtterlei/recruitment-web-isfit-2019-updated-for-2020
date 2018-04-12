from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from job.models import Application#, Ranking
from django.forms import inlineformset_factory
from .models import Position, Gang, Section
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
    trondheim = forms.BooleanField(label="Do you currently live in Trondheim?", help_text="Yes")
    student = forms.BooleanField(label="Are you a student?", help_text="Yes")

    class Meta:
        model = Application#, Ranking
        exclude = ['applicant']
        fields = ('text', 'phone_number', 'trondheim', 'student')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['trondheim'].widget.attrs.update({'class': 'form-control'})
        self.fields['student'].widget.attrs.update({'class': 'form-control'})


'''class RankingForm(forms.ModelForm):
    rank = forms.IntegerField(max_value=3, min_value=1)
    user = User.objects.get(id=4)
    application = Application.objects.get(id=user.pk)
    position = forms.ModelMultipleChoiceField(queryset=application.positions.all())


    class Meta:
        model = Ranking
        exclude = ['applicant']
        fields = ('rank', 'position')

    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs)
        self.fields['rank'].widget.attrs.update({'class': 'form-control'})
        #application = Application.objects.first()
        #self.fields['position'].queryset = application.positions.all()

RankFormSet = inlineformset_factory(Application, Ranking, fields=('rank',))
rankForPosition = Ranking.objects.get(position=Ranking.position)
formset = RankFormSet(instance=rankForPosition)'''




















