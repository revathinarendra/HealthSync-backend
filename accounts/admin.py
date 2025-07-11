from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile


class AccountAdmin(UserAdmin):
    list_display = ("email", "username", "role","date_joined", "last_login", "is_admin", "is_staff")
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_staff", "is_active", "is_superadmin")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    ordering = ("email",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "state", "country")
    search_fields = ("user__email", "user__username", "city", "state", "country")


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
