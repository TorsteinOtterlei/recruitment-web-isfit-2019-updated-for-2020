from django.contrib import admin
from .models import *


class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    filter_horizontal = ('jobs',)

admin.site.register(Gang)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Job)
admin.site.register(Section)
admin.site.register(Project)
