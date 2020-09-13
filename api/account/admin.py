from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import *

from django.contrib.auth.models import Group
admin.site.unregister(Group)


class AccountAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreateForm

    readonly_fields=('date_joined', 'last_login' )
    
    list_display = ['email', 'is_admin', 'is_staff', 'is_superuser', 'is_active']
    list_filter = ['is_superuser','is_admin', 'is_staff', 'is_active']
    fieldsets = (
        ('Account information', {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        ('Important dates', {'fields': ('date_joined', 'last_login' )}),
        ('Permissions', {'fields': ('is_superuser','is_admin', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ('Account information', {
            'fields': ('email', 'password1', 'password2')}
        ),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    search_fields = ('email',)
    ordering = ('date_joined',)

admin.site.register(Account, AccountAdmin)