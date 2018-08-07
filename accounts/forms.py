from django.contrib.auth.forms import UserCreationForm
from django import forms
# local:
from accounts.models import User
# other apps:
from jobs.models import Section

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250, required=True, help_text='Required')
    first_name = forms.CharField(max_length=50, required=True, help_text='Required')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required')
    phone_number = forms.CharField(max_length=12)

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

class StatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=User.STATUS_CHOISES)
    # Only giving class name for CSS access
    status.widget.attrs.update({'class': 'status-field'})

    class Meta:
        model = User
        fields = (['status'])

class WidgetsForm(forms.Form):
    bool = forms.BooleanField()
    char = forms.CharField()
    choice = forms.ChoiceField(choices=User.STATUS_CHOISES)
    typedChoice = forms.TypedChoiceField(choices=User.STATUS_CHOISES)
    date = forms.DateField()
    datetime = forms.DateTimeField()
    decimal = forms.DecimalField()
    duration = forms.DurationField()
    email = forms.EmailField()
    file = forms.FileField()
    filepath = forms.FilePathField(path="C:/Users/emilt/isfit/recruitment-web-isfit-2019")
    float = forms.FloatField()
    image = forms.ImageField()
    integer = forms.IntegerField()
    genericIP = forms.GenericIPAddressField()
    multipleChoice = forms.MultipleChoiceField(choices=User.STATUS_CHOISES)
    typedMultipleChoice = forms.TypedMultipleChoiceField(choices=User.STATUS_CHOISES)
    nullBool = forms.NullBooleanField()
    regex = forms.RegexField(regex=r".")
    slug = forms.SlugField()
    time = forms.TimeField()
    url = forms.URLField()
    uuid = forms.UUIDField()
    combo = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()])
    #multivalue = forms.MultiValueField()
    splitDateTime = forms.SplitDateTimeField()
    modelChoice = forms.ModelChoiceField(queryset=Section.objects.all())
    modelMultipleChoice = forms.ModelMultipleChoiceField(queryset=Section.objects.all())
