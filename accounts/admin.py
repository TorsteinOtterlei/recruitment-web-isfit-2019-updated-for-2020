from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from import_export.admin import ImportExportModelAdmin
# local:
from accounts.models import User
from accounts.forms import SignUpForm

def make_staff(modeladmin, request, queryset):
    queryset.update(staff=True)
    make_staff.short_description = "Mark selected users as staff"

class UserAdmin(ImportExportModelAdmin): # Replaced auth_admin.UserAdmin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),

        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'gang')}),
        ('Permissions', {'fields': ('active', 'staff', 'superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}
        ),
    )
    add_form = SignUpForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'staff', 'superuser')
    list_filter = ('recruiter', 'interviewer', 'staff', 'superuser', 'active', 'groups')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ['email']
    readonly_fields = ['last_login', 'date_joined']
    actions = [make_staff]

# Register your models here.
admin.site.register(User, UserAdmin)
