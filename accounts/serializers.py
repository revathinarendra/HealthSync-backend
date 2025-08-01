# accounts/serializers.py

from rest_framework import serializers
from .models import Account, UserProfile, PasswordResetOTP , Cities, Professions
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
import datetime


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields=['id','city']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Professions
        fields=['id','profession']





# --- Existing AccountSerializer ---
class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=True, allow_blank=False, max_length=100)
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    
    class Meta:
        model = Account
        # Include 'dietician_id' in fields if it's meant to be serialized
        fields = ["dietician_id", "id", "email", "username", "role", "password", "date_joined", "last_login", "is_admin", "is_staff", "is_active", "is_superadmin", "gender", "DOB", "phone_number", "profession", "location"]
        read_only_fields = ["id", "date_joined", "last_login", "is_admin", "is_staff", "is_active", "is_superadmin", "dietician_id"]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data.pop('username')
        email = validated_data.pop('email')       
        role = validated_data.pop('role', 'customer') 
        DOB = validated_data.pop('DOB', None)
        profession = validated_data.pop('profession', None)
        location = validated_data.pop('location', None)
        phone_number = validated_data.pop('phone_number', None)
        gender = validated_data.pop('gender', None)
        is_superadmin_val = validated_data.pop('is_superadmin', False)

        if not username:
            raise serializers.ValidationError({"username": "Username is required if password is not provided."})
        
        if not password: # Provide a default password if none is given (e.g., if only email/username are supplied)
            password = f"{username}@qwertyuiop"

        is_admin_status = False
        is_staff_status = False
        is_active_status = True 

        if role in ['dietitian', 'admin']:
            is_admin_status = True
            is_staff_status = True

        creating_user = self.context.get('request').user if 'request' in self.context else None
        
        # Set 'dietician_id' if the creating user is a dietitian, admin, or superadmin
        if creating_user and creating_user.is_authenticated and (creating_user.role == 'dietitian' or creating_user.is_admin or creating_user.is_superadmin):
            validated_data['dietician_id'] = creating_user.id
        else:
            validated_data['dietician_id'] = None # Or handle as appropriate

        user = Account.objects.create_user(
            email=email,        
            username=username,  
            password=password,
            role=role,
            DOB=DOB,
            profession=profession,
            location=location,
            phone_number=phone_number,
            gender=gender,
            is_active=is_active_status, 
            is_staff=is_staff_status,   
            is_admin=is_admin_status,   
            is_superadmin=is_superadmin_val,
            **validated_data # Pass remaining validated_data which now includes dietician_id
        )
        return user 

# --- Existing UserProfileSerializer ---
class UserProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = UserProfile
        # Ensure these fields match your current UserProfile model
        fields = ["user", "name", "gender", "DOB", "phone_number", "profession", "city"]

# --- Existing LoginSerializer ---
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            if not Account.objects.filter(email=email).exists():
                raise serializers.ValidationError('No user found with this email address.')

        return data

# --- NEW: Serializer for requesting OTP ---
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            Account.objects.get(email=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value

# --- NEW: Serializer for verifying OTP ---
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp_code = data.get('otp')

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

        # Check for a valid and active OTP
        # Order by created_at descending to get the latest OTP first
        otp_instance = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp_code,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()

        if not otp_instance:
            raise serializers.ValidationError("Invalid or expired OTP.")
        
        data['user'] = user # Attach user object for view
        data['otp_instance'] = otp_instance # Attach otp instance for view
        return data

# --- NEW: Serializer for resetting password after OTP verification ---
class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New passwords do not match."})
        
        # Use the VerifyOTPSerializer's validation logic to verify email and OTP
        verify_serializer = VerifyOTPSerializer(data={'email': data['email'], 'otp': data['otp']})
        verify_serializer.is_valid(raise_exception=True) # Raise exception if OTP is invalid

        user = verify_serializer.validated_data['user']
        otp_instance = verify_serializer.validated_data['otp_instance']

        try:
            validate_password(data['new_password'], user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        data['user'] = user
        data['otp_instance'] = otp_instance
        return data

    def save(self):
        user = self.validated_data['user']
        otp_instance = self.validated_data['otp_instance']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.is_active = True # Optionally activate user if they were inactive (e.g., first login)
        user.save()

        # Mark OTP as used
        otp_instance.is_used = True
        otp_instance.save()

        return user