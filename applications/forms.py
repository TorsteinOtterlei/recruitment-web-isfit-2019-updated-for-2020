from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import inlineformset_factory
from .models import *
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField

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

"""
class RankingForm(forms.ModelForm):
    #first = Position.objects.get(id=1)
    #second = Position.objects.get(id=1)
    #third = Position.objects.get(id=1)

    class Meta:
        model = Ranking
        exclude = []
        fields = ('first', 'second', 'third')

    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs)


#RankFormSet = inlineformset_factory(Application, Ranking, fields=('rank',))
#rankForPosition = Ranking.objects.get(position=Ranking.position)
#formset = RankFormSet(instance=rankForPosition)
"""
