from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# If you previously registered User, unregister it first
from django.contrib.auth import get_user_model
try:
    admin.site.unregister(get_user_model())
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # only show fields that exist on User
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_superuser')  # remove 'address'
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone',)}),  # remove 'address'
    )
