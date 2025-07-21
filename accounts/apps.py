# accounts/apps.py

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Application configuration for the accounts app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'