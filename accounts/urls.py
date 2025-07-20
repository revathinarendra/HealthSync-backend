# accounts/urls.py

from django.urls import path
from . import views


# URL patterns for the accounts application
urlpatterns = [
    # --- Authentication & Registration ---
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # --- Profile & Account Management ---
    path('profile/', views.user_profile, name='user_profile'),
    path('list-accounts/', views.list_accounts, name='list_accounts'), # Requires authentication/permissions

    # --- Password Reset ---
    path('request-password-reset-otp/', views.request_password_reset_otp, name='request_password_reset_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password-confirm/', views.reset_password_confirm, name='reset_password_confirm'),

    # --- Utility Data Lists (e.g., for dropdowns) ---
    path('list-professions/', views.ProfessionsListView.as_view(), name='list_professions'),
    path('list-cities/', views.CitiesListView.as_view(), name='list_cities'),
]