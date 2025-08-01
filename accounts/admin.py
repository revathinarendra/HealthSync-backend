# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile


from .models import PasswordResetOTP, Cities, Professions
class AccountAdmin(UserAdmin):
    list_display = ( "dietician_id","id", "email", "username", "role","date_joined", "last_login", "is_admin", "is_staff","profession", "gender", "DOB", "phone_number","location") # CORRECTED: Added id and created_by
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("dietician_id","email", "username", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_staff", "is_active", "is_superadmin", "role")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password", "role", "is_staff", "is_active", "is_superadmin", "is_admin"), # Added password, role, is_superadmin, is_admin
        }),
    )

    ordering = ("email",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "gender", "DOB", "phone_number", "profession", "city") # Updated for UserProfile fields
    search_fields = ("user__email", "user__username", "name", "city", "profession")


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PasswordResetOTP)
admin.site.register(Cities)
admin.site.register(Professions)
