from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from import_export.admin import ImportExportModelAdmin
# local:
from accounts.models import User
from accounts.forms import SignUpForm, EditUserForm

# Actions for Admin-site:
def make_staff(modeladmin, request, queryset):
    queryset.update(staff=True)
    make_staff.short_description = "Mark selected users as staff"

def make_superuser(modeladmin, request, queryset):
    queryset.update(superuser=True)
    make_superuser.short_description = "Mark selected users as superuser"

def make_recruiter(modeladmin, request, queryset):
    queryset.update(recruiter=True)
    make_recruiter.short_description = "Mark selected users as recruiter"

def make_interviewer(modeladmin, request, queryset):
    queryset.update(interviewer=True)
    make_interviewer.short_description = "Mark selected users as interviewer"

# -------------------------------------------------------------------------------------------------------------------------------

# BUG: ImportExportModelAdmin can NOT replace auth_admin.UserAdmin
class UserAdmin(auth_admin.UserAdmin, ImportExportModelAdmin):
    # User forms
    form = auth_admin.UserChangeForm
    add_form = SignUpForm # Important! (AbstractBaseUser is created differently)
    change_password_form = auth_admin.AdminPasswordChangeForm

    # Fields shown in user detail: admin/accounts//user/'id'/change
    fieldsets = (
        (None,              {'fields': ('email', 'password')}),
        ('Personal info',   {'fields': ['first_name', 'last_name', 'phone_number', 'gang', 'status']}),
        ('Permissions',     {'fields': ('active', 'staff', 'superuser', 'recruiter', 'interviewer',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # No idea what this is for
    limited_fieldsets = (
        (None,              {'fields':   ('email',)}),
        ('Personal info',   {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Not sure what this is for
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'staff', 'superuser')
    list_filter = ('recruiter', 'interviewer', 'staff', 'superuser', 'active', 'groups')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ['email']
    readonly_fields = ['last_login', 'date_joined']
    filter_horizontal = ('groups', 'user_permissions')
    actions = [make_staff]

# Register your models here.
admin.site.register(User, UserAdmin)
