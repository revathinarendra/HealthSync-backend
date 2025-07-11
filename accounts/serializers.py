from rest_framework import serializers
from .models import Account, UserProfile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "username", "date_joined", "last_login", "is_admin", "is_staff", "is_active", "is_superadmin"]
        read_only_fields = ["date_joined", "last_login"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "address_line_1", "address_line_2", "profile_picture", "city", "state", "country"]


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