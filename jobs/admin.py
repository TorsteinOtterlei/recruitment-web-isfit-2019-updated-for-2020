from django.db import models
from django.contrib import admin
# local
from jobs.models import Section, Gang, Position, Project, Calendar

admin.site.register(Section)
admin.site.register(Gang)
admin.site.register(Position)
admin.site.register(Project)
admin.site.register(Calendar)
