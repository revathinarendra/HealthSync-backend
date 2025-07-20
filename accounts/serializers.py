# accounts/serializers.py

from rest_framework import serializers
from .models import Account, UserProfile, PasswordResetOTP, Cities, Professions
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
import datetime


# --- Utility Serializers for Data Models ---
class CitiesSerializer(serializers.ModelSerializer):
    """Serializer for the Cities model."""
    class Meta:
        model = Cities
        fields = ['id', 'city']


class ProfessionSerializer(serializers.ModelSerializer):
    """Serializer for the Professions model."""
    class Meta:
        model = Professions
        fields = ['id', 'profession']


# --- User Account Serializers ---
class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model. Handles user registration and account details.
    """
    password = serializers.CharField(write_only=True, required=False) # Password is write-only
    email = serializers.EmailField(required=True, allow_blank=False, max_length=100)
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)

    class Meta:
        model = Account
        # Include all relevant fields. 'dietician_id' should only be here if it's a direct field in Account model.
        # Based on models.py, it's not. If it's a reference to a dietitian, it needs to be explicit.
        # For now, removed it as it's not in the model.
        fields = ["id", "email", "username", "role", "password", "date_joined",
                  "last_login", "is_admin", "is_staff", "is_active", "is_superadmin"]
        read_only_fields = ["id", "date_joined", "last_login", "is_admin", "is_staff",
                            "is_active", "is_superadmin"] # These fields are set internally or by Django

    def create(self, validated_data):
        """
        Custom create method for AccountSerializer to handle password hashing and role-based permissions.
        """
        password = validated_data.pop('password', None)
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        role = validated_data.pop('role', 'customer')
        is_superadmin_val = validated_data.pop('is_superadmin', False)

        if not username:
            raise serializers.ValidationError({"username": "Username is required if password is not provided."})

        # Set a default password if none is provided during creation
        # IMPORTANT: In a real-world scenario, you might want to remove this
        # or generate a truly random secure password for initial setup.
        if not password:
            password = f"{username}@qwertyuiop"

        # Determine initial permission flags based on role
        is_admin_status = False
        is_staff_status = False
        is_active_status = True # Typically set to False for email verification flow, then activated

        if role in ['dietitian', 'admin']:
            is_admin_status = True
            is_staff_status = True

        user = Account.objects.create_user(
            email=email,
            username=username,
            password=password,
            role=role,
            is_active=is_active_status,
            is_staff=is_staff_status,
            is_admin=is_admin_status,
            is_superadmin=is_superadmin_val,
            **validated_data # Pass remaining validated_data (if any)
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    Includes the associated Account details as a read-only nested serializer.
    """
    user = AccountSerializer(read_only=True)
    DOB = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])

    class Meta:
        model = UserProfile
        # Ensure fields here match your UserProfile model fields
        fields = ["user", "name", "gender", "DOB", "phone_number", "profession", "city"]


# --- Authentication Serializers ---
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Validates email and password.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Check if user exists before attempting authentication for better error messages
            if not Account.objects.filter(email=email).exists():
                raise serializers.ValidationError('No user found with this email address.')
        return data


# --- Password Reset Serializers ---
class RequestPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset OTP.
    Validates that the email exists in the system.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Validates if an Account with the given email exists.
        """
        try:
            self.user = Account.objects.get(email=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer for verifying a password reset OTP.
    Validates email, OTP, expiry, and usage status.
    """
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        email = data.get('email')
        otp_code = data.get('otp')

        if not (email and otp_code):
            raise serializers.ValidationError("Both email and OTP are required.")

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"email": "No user found with this email address."})

        # Get the latest valid OTP for the user that is not used and not expired
        otp_instance = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp_code,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first() # Get the most recent one

        if not otp_instance:
            raise serializers.ValidationError({"otp": "Invalid or expired OTP."})

        # Attach user and otp_instance to validated_data for later use
        data['user'] = user
        data['otp_instance'] = otp_instance
        return data


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset and setting a new password.
    Validates email, OTP, and new password against Django's password validators.
    """
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        # 1. Check if new passwords match
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New passwords do not match."})

        # 2. Use VerifyOTPSerializer's validation logic to verify email and OTP
        # This reuses logic and ensures OTP validity before proceeding
        verify_serializer = VerifyOTPSerializer(data={'email': data['email'], 'otp': data['otp']})
        verify_serializer.is_valid(raise_exception=True) # Raise exception if OTP is invalid

        user = verify_serializer.validated_data['user']
        otp_instance = verify_serializer.validated_data['otp_instance']

        # 3. Validate new password against Django's validators
        try:
            validate_password(data['new_password'], user=user)
        except DjangoValidationError as e:
            # Convert Django's validation errors into a DRF-compatible format
            raise serializers.ValidationError({"new_password": list(e.messages)})

        # Attach user and otp_instance to validated_data for use in save method
        data['user'] = user
        data['otp_instance'] = otp_instance
        return data

    def save(self):
        """
        Resets the user's password and marks the OTP as used.
        """
        user = self.validated_data['user']
        otp_instance = self.validated_data['otp_instance']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        # Optionally activate user if they were inactive (e.g., after initial registration, before first login)
        if not user.is_active:
            user.is_active = True
        user.save()

        # Mark OTP as used to prevent reuse
        otp_instance.is_used = True
        otp_instance.save()

        return user