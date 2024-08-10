from django.contrib import admin
from .models import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    # Define the fields to display in the admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff' ,'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new user
            obj.is_staff = True  # Ensure the user can log in to the admin site
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
