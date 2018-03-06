from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from django.db import models

class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    readonly_fields = ('positions','applicant', 'phone_number','text', )

    filter_horizontal = ('positions',) #was jobs
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'200'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


admin.site.register(Gang)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Position)
admin.site.register(Section)
admin.site.register(Project)
