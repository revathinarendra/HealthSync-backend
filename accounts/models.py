# accounts/models.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from dry import settings
import random
import string


# --- Custom User Manager ---
class MyAccountManager(BaseUserManager):
    """
    Custom manager for the Account model, handling user creation (normal and superuser).
    """
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email, username, and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        # Create a copy to safely pop fields used for model instantiation
        cleaned_extra_fields = extra_fields.copy()
        cleaned_extra_fields.pop('email', None)
        cleaned_extra_fields.pop('username', None)

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **cleaned_extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, username, and password.
        Sets default superuser specific fields.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('role', 'admin') # Superuser role should typically be 'admin'

        return self.create_user(email, username, password, **extra_fields)


# --- Account Model (Custom User Model) ---
class Account(AbstractBaseUser):
    """
    Custom user model for the application.
    Uses email as the unique identifier for authentication.
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('dietitian', 'Dietitian'),
        ('admin', 'Admin'), # Role for superusers
    )

    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) # Accounts might be inactive until email verification or admin approval
    is_superadmin = models.BooleanField(default=False)
    dietician_id = models.IntegerField(null=True, blank=True) # Optional field for dietician ID

    USERNAME_FIELD = "email" # Use email for login
    REQUIRED_FIELDS = ["username"] # Fields required when creating a user via createsuperuser command

    objects = MyAccountManager() # Assign the custom manager

    def save(self, *args, **kwargs):
        """
        Overrides save to ensure username defaults to email if not provided.
        """
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Account object.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Checks if the user has a specific permission.
        Simplistic check: assumes admin users have all permissions.
        """
        return self.is_admin

    def has_module_perms(self, add_label):
        """
        Checks if the user has permissions to view a given app (`add_label`).
        Simplistic check: assumes all users with any permissions can view all modules.
        """
        return True

    # Convenience methods for role checking
    def is_dietician(self):
        """Checks if the user's role is 'dietitian'."""
        return self.role == 'dietitian'

    def is_customer(self):
        """Checks if the user's role is 'customer'."""
        return self.role == 'customer'


# --- User Profile Model ---
class UserProfile(models.Model):
    """
    Extends the Account model with additional user-specific details.
    Uses a OneToOneField to link directly to an Account.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userprofile")
    name = models.CharField(blank=True, null=True, max_length=100)
    gender = models.CharField(blank=True, null=True, max_length=100)
    DOB = models.DateField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    profession = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        """
        String representation of the UserProfile object.
        Returns the profile name or the associated user's email if name is not set.
        """
        return self.name if self.name else self.user.email

# --- Signal to Create UserProfile Automatically ---
@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to automatically create a UserProfile whenever a new Account is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


# --- Password Reset OTP Model ---
class PasswordResetOTP(models.Model):
    """
    Stores One-Time Passwords (OTPs) for password reset functionality.
    Includes expiry time and usage status.
    """
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6) # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Overrides save to set the expiry time for the OTP when it's first created.
        OTP is valid for 10 minutes from creation.
        """
        if not self.id:  # Only set expires_at on first save
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the PasswordResetOTP object.
        """
        return f"OTP for {self.user.email}: {self.otp}"


# --- Utility Models for Dropdowns/Categorization ---
class Cities(models.Model):
    """
    Model to store a list of cities.
    Used for predefined choices in user profiles or other forms.
    """
    city = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True) # To activate/deactivate city options

    class Meta:
        ordering = ['city']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city


class Professions(models.Model):
    """
    Model to store a list of professions.
    Used for predefined choices in user profiles or other forms.
    """
    profession = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True) # To activate/deactivate profession options

    class Meta:
        ordering = ['profession']
        verbose_name = 'Profession'
        verbose_name_plural = 'Professions'

    def __str__(self):
        return self.profession