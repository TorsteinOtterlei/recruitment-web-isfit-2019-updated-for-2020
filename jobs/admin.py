from django.db import models
from django.contrib import admin
# local
from jobs.models import Section, Gang, Position, Project, Calendar, Date

admin.site.register(Section)
admin.site.register(Gang)
admin.site.register(Project)
#admin.site.register(Calendar)
admin.site.register(Date)

"""
    title = models.CharField(max_length=50)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name="positions")
    description = models.TextField(max_length=20000)
    interviewer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="position", blank=True)
"""

class PositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['title', 'description'] } ),
        ('Relations', {'fields': ['interviewer', 'gang'] } ),
    )
    list_display = ['interviewer', 'title', 'section', 'gang']
    list_filter = ['gang']
    search_fields = ['interviewer__email', 'interviewer__full_name', 'interviewer__phone_number']
    ordering = ['gang']
    readonly_fields = []

    def section(self, position):
        return position.gang.section.name


admin.site.register(Position, PositionAdmin)
