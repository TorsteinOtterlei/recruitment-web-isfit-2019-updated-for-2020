from django.contrib import admin
# local:
from apps.applications.models import Application, CloseTime

from datetime import date
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from apps.jobs.models import Section, Gang

class ApplicationSectionFilter(admin.SimpleListFilter):
    title = _('section')
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        return [(section.id, section.name) for section in Section.objects.all()]

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset

        for section in Section.objects.all():
            if str(self.value()) == str(section.id):
                return queryset.filter( Q(first__gang__section=section) | Q(second__gang__section=section) | Q(third__gang__section=section) )


class ApplicationGangFilter(admin.SimpleListFilter):
    title = _('gang')
    parameter_name = 'gang'

    def lookups(self, request, model_admin):
        return [(gang.id, gang.name) for gang in Gang.objects.all()]

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset

        for gang in Gang.objects.all():
            if str(self.value()) == str(gang.id):
                return queryset.filter( Q(first__gang=gang) | Q(second__gang=gang) | Q(third__gang=gang) )


class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['applicant'] } ),
        ('Positions', {'fields': ['first', 'second', 'third'] } ),
        ('Application information', {'fields': ['text', 'interview_time'] } ),
    )
    list_display = ['applicant', 'first', 'second', 'third', 'pretty_interview_time', 'interview_time']
    list_filter = [ApplicationSectionFilter, ApplicationGangFilter]
    search_fields = ['applicant__email', 'applicant__first_name','applicant__last_name', 'applicant__phone_number']
    ordering = ['interview_time']
    readonly_fields = ['interview_time']

admin.site.register(CloseTime)
admin.site.register(Application, ApplicationAdmin)
