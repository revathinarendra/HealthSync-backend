from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile-name/', views.get_user_profile_name_by_id, name='get_user_profile_name_by_id'),
    path('login/', views.login_view, name='login'),
    path('list-accounts/', views.list_accounts, name='list_accounts'),
    path('request-password-reset-otp/', views.request_password_reset_otp, name='request_password_reset_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password-confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('list-professions/', views.ProfessionsListView.as_view(), name='list_professions'),
    path('list-cities/', views.CitiesListView.as_view(), name='list_cities'),
]