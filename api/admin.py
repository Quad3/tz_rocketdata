from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Address,
    Contact,
    Producer,
    Product,
    Employee,
)


class CustomUserAdmin(UserAdmin):
    model = Employee
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'producer',
        'is_staff',
        'is_active',
    ]
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "producer")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
                "classes": ("wide",),
                "fields": (
                    "email", "password1", "password2", "first_name", "last_name", "producer"
                )}
        ),
    )
    ordering = ['id']



admin.site.register([
    Address,
    Contact,
    Producer,
    Product,
])
admin.site.register(Employee, CustomUserAdmin)
