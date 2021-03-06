from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from import_export.admin import ImportExportModelAdmin
# local:
from apps.accounts.models import User
from apps.accounts.forms import SignUpForm, EditUserForm

# Actions for Admin-site:
def make_staff(modeladmin, request, queryset):
    queryset.update(staff=True)
    make_staff.short_description = "Mark selected users as staff"

def make_normal_user(modeladmin, request, queryset):
    queryset.update(staff=False)
    queryset.update(superuser=False)
    make_normal_user.short_description = "Mark selected users as normal users without any permissions"

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
    add_form = auth_admin.UserCreationForm # Important!
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

    list_display = ('email', 'get_full_name', 'phone_number', 'gang', 'staff', 'superuser')
    list_filter = ('staff', 'superuser', 'status', 'gang', 'active', 'recruiter', 'interviewer')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ['email']
    readonly_fields = ['last_login', 'date_joined']
    filter_horizontal = ('groups', 'user_permissions')
    actions = [make_normal_user, make_staff, make_superuser, make_recruiter, make_interviewer]

# Register your models here.
admin.site.register(User, UserAdmin)
