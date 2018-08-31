from django.db import models
from django.contrib import admin
# local
from jobs.models import Section, Gang, Position, Project, Calendar, Date, Interview

admin.site.register(Section)
admin.site.register(Gang)
admin.site.register(Project)
admin.site.register(Interview)
#admin.site.register(Calendar)


class PositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['title', 'description', 'comment', 'weight'] } ),
        ('Relations', {'fields': ['interviewers', 'contact_person', 'gang'] } ),
    )
    filter_horizontal = ['interviewers']
    list_display = ['title', 'section', 'gang', 'contact_person']
    list_filter = ['gang__section', 'gang']
    search_fields = ['title' ,'contact_person__email', 'contact_person__first_name', 'contact_person__last_name', 'contact_person__phone_number']
    ordering = ['gang']
    readonly_fields = []

    def section(self, position):
        return position.gang.section.name

class DateAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User', {'fields': ['user'] } ),
        ('List of available times for interview', {'fields': ['dates'] } ),
    )
    list_display = ['user', 'dates']
    list_filter = []
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'user__phone_number']
    ordering = ['user']
    readonly_fields = ['dates']


admin.site.register(Position, PositionAdmin)
admin.site.register(Date, DateAdmin)
