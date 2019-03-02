from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
# local:
from apps.accounts.models import User
# other apps:
from apps.jobs.models import Section

class SignUpForm(UserCreationForm):
    trondheim = forms.BooleanField(required=True, help_text='Yes I live in Trondheim, and know that this page is for volunteering and NOT participating', error_messages={'required': 'You have to live in Trondheim to volunteer'})

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password1',
            'password2',
            'trondheim'
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = 'Your password cant be too similar to your other personal information. Your password must contain atleast 8 characters. Your password cant be a commonly used password and cant be entierly numeric.'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})

class StatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=User.STATUS_CHOISES)
    # Only giving class name for CSS access
    status.widget.attrs.update({'class': 'status-field'})

    class Meta:
        model = User
        fields = ['status']

class RestrictedStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=User.RESTRICTED_STATUS_CHOISES)
    # Only giving class name for CSS access
    status.widget.attrs.update({'class': 'status-field'})

    class Meta:
        model = User
        fields = ['status']

# Possible to customise login:
class CustomAuthenticationForm(AuthenticationForm): # Not currently in use. Can be passed to login view
    error_messages = dict(AuthenticationForm.error_messages) # Inherit from parent. invalid_login and inactive

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

        if not user.is_authenticated:
            raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

class CustomPasswordChangeForm(PasswordChangeForm):
    # Inherited fields:
    # old_password
    # new_password1
    # new_password2

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class EmailForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        #for field in self.fields.values():
            #field.widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'id': 'field-body', 'class': 'form-control'})


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
