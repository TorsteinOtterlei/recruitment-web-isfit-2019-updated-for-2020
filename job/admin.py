from django.contrib import admin
from .models import Applicant, Application, Job, Job_Detail

# Register your models here.
admin.site.register(Applicant)
admin.site.register(Application)
admin.site.register(Job)
admin.site.register(Job_Detail)