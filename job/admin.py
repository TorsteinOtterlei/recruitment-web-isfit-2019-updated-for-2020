from django.contrib import admin
from .models import Application, Job, Gang

# Register your models here.
admin.site.register(Gang)
admin.site.register(Application)
admin.site.register(Job)