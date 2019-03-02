from django import forms
from apps.applications.models import Application

class ApplicationForm(forms.ModelForm):
    text = forms.CharField(label="Why do you want to volunteer with ISFiT? Write a brief text and then choose the positions you want to apply for.", max_length=2000, required=True, widget=forms.Textarea())

    class Meta:
        model = Application
        fields = (
            'text',
        )
        exclude = ['applicant']

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        #self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
