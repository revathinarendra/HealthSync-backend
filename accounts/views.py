# accounts/views.py

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random
import string

from .models import Account, UserProfile, PasswordResetOTP, Cities, Professions
from .serializers import (
    AccountSerializer,
    LoginSerializer,
    UserProfileSerializer,
    RequestPasswordResetSerializer,
    VerifyOTPSerializer,
    ResetPasswordConfirmSerializer,
    CitiesSerializer,
    ProfessionSerializer,
)


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def send_otp_email(email, otp_code):
    """
    Sends a One-Time Password (OTP) to the specified email address.

    Args:
        email (str): The recipient's email address.
        otp_code (str): The 6-digit OTP to be sent.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    subject = 'Your Password Reset OTP'
    message = f'Hi,\n\nYour One-Time Password (OTP) for password reset is: {otp_code}\n\nThis OTP is valid for 10 minutes. Do not share this with anyone.\n\nThank you,\nYour Application Team'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}") # Log the error for debugging
        return False


# ==============================================================================
# AUTHENTICATION & ACCOUNT MANAGEMENT VIEWS
# ==============================================================================

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def register(request):
    """
    Handles user registration.
    Allows superadmin to create admin/dietitian/customer, admin to create dietitian/customer,
    and dietitian to create customers.
    """
    data = request.data
    requested_role = data.get('role', 'customer')

    if requested_role not in dict(Account.ROLE_CHOICES).keys():
        return Response({'error': 'Invalid role specified.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

    # --- Authorization Logic ---
    if requested_role == 'admin' and not user.is_superadmin:
        return Response({'error': 'You do not have permission to create admin accounts.'}, status=status.HTTP_403_FORBIDDEN)

    if requested_role == 'dietitian' and not (user.is_admin or user.is_superadmin):
        return Response({'error': 'You do not have permission to create dietitian accounts.'}, status=status.HTTP_403_FORBIDDEN)

    if requested_role == 'customer' and not (user.role == 'dietitian' or user.is_superadmin):
        return Response({'error': 'Only dietitian or admin/superadmin can register customers.'}, status=status.HTTP_403_FORBIDDEN)

    user_serializer = AccountSerializer(data=data, context={'request': request})

    if user_serializer.is_valid():
        user = user_serializer.save()
        return Response({
            'message': 'User registered successfully.',
            'user_id': user.id,
            'email': user.email,
            'role': user.role
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """Handles user login and issues JWT tokens."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'role': user.role,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_password_reset_otp(request):
    """Requests an OTP for password reset and sends it to the user's email."""
    serializer = RequestPasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = Account.objects.get(email=email)

        # Invalidate any existing active OTPs for this user
        PasswordResetOTP.objects.filter(user=user, is_used=False, expires_at__gt=timezone.now()).update(is_used=True)

        # Generate a new 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        PasswordResetOTP.objects.create(user=user, otp=otp_code)

        if send_otp_email(email, otp_code):
            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to send OTP email. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    """Verifies a provided OTP for password reset."""
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password_confirm(request):
    """Resets the user's password after OTP verification."""
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() # This method also marks OTP as used
        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==============================================================================
# USER PROFILE VIEWS
# ==============================================================================

@api_view(['GET', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Handles retrieval (GET) and partial update (PATCH) of the authenticated user's profile.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer  = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==============================================================================
# ADMIN & DIETITIAN VIEWS
# ==============================================================================

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_accounts(request):
    """
    Lists accounts based on the requesting user's role:
    - Superadmins see all accounts.
    - Dietitians see customer accounts created by them.
    """
    user = request.user
    accounts = Account.objects.all().order_by('id')

    if user.is_superadmin:
        pass # Superadmin can see all accounts
    elif user.role == 'dietitian':
        accounts = accounts.filter(created_by=user, role='customer')
    else:
        return Response({'error': 'You do not have permission to view this list.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================================================================
# LOOKUP DATA VIEWS (Cities & Professions)
# ==============================================================================

class CitiesListView(generics.ListAPIView):
    """Lists all active cities."""
    queryset = Cities.objects.filter(is_active=True)
    serializer_class = CitiesSerializer


class ProfessionsListView(generics.ListAPIView):
    """Lists all active professions."""
    queryset = Professions.objects.filter(is_active=True)
    serializer_class = ProfessionSerializer