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
        (None, {'fields': ['title', 'description', 'comment'] } ),
        ('Relations', {'fields': ['interviewers', 'interviewer', 'gang'] } ),
    )
    filter_horizontal = ['interviewers']
    list_display = ['title', 'section', 'gang', 'interviewer']
    list_filter = ['gang']
    search_fields = ['title' ,'interviewer__email', 'interviewer__first_name', 'interviewer__last_name', 'interviewer__phone_number']
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
