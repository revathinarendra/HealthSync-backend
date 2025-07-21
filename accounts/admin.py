# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile, PasswordResetOTP, Cities, Professions # Import all models


# --- Account Admin Configuration ---
class AccountAdmin(UserAdmin):
    """
    Custom Admin configuration for the Account model.
    Customizes display, search, read-only fields, and fieldsets for the Django admin.
    """
    # Fields to display in the list view of accounts in the admin panel
    list_display = (
        "id", "email", "username", "role", "date_joined",
        "last_login", "is_admin", "is_staff", "is_active", "is_superadmin"
    )
    # Fields to search by in the admin panel
    search_fields = ("email", "username")
    # Fields that cannot be edited after creation
    readonly_fields = ("date_joined", "last_login")

    # Disable default Django UserAdmin filters/fieldsets not relevant here
    filter_horizontal = ()
    list_filter = ("role", "is_admin", "is_staff", "is_active", "is_superadmin") # Add useful filters

    # Custom fieldsets for displaying and editing Account details
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_staff", "is_active", "is_superadmin", "role")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Custom fieldsets for adding new Account instances
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password", "role", "is_staff", "is_active", "is_superadmin", "is_admin"),
        }),
    )

    # Default ordering for accounts in the list view
    ordering = ("email",)


# --- User Profile Admin Configuration ---
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserProfile model.
    """
    # Fields to display in the list view of user profiles
    list_display = ("user", "name", "gender", "DOB", "phone_number", "profession", "city")
    # Fields to search by
    search_fields = ("user__email", "user__username", "name", "city", "profession")
    # Fields for filtering
    list_filter = ("gender", "profession", "city")
    # Allow editing of fields directly in the list display (if desired)
    list_editable = ("gender", "profession", "city")


# --- Password Reset OTP Admin Configuration ---
class PasswordResetOTPAdmin(admin.ModelAdmin):
    """
    Admin configuration for the PasswordResetOTP model.
    """
    list_display = ("user", "otp", "created_at", "expires_at", "is_used")
    search_fields = ("user__email", "otp")
    list_filter = ("is_used", "created_at", "expires_at")
    readonly_fields = ("created_at", "expires_at") # These fields are set automatically

# --- Utility Models Admin Configuration ---
class CitiesAdmin(admin.ModelAdmin):
    """Admin configuration for the Cities model."""
    list_display = ('city', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('city',)
    ordering = ('city',)
    list_editable = ('is_active',)

class ProfessionsAdmin(admin.ModelAdmin):
    """Admin configuration for the Professions model."""
    list_display = ('profession', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('profession',)
    ordering = ('profession',)
    list_editable = ('is_active',)


# --- Register Models with Admin Site ---
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PasswordResetOTP, PasswordResetOTPAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Professions, ProfessionsAdmin)