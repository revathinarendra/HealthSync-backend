# accounts/views.py

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Account,UserProfile, PasswordResetOTP , Cities, Professions
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
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.utils import timezone

class CitiesListView(generics.ListAPIView):
    queryset = Cities.objects.filter(is_active=True)
    serializer_class = CitiesSerializer


class ProfessionsListView(generics.ListAPIView):
    queryset = Professions.objects.filter(is_active=True)
    serializer_class = ProfessionSerializer

# --- Helper function to send OTP email ---
def send_otp_email(email, otp_code):
    subject = 'Your Password Reset OTP'
    message = f'Hi,\n\nYour One-Time Password (OTP) for password reset is: {otp_code}\n\nThis OTP is valid for 10 minutes. Do not share this with anyone.\n\nThank you,\nYour Application Team'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# --- Existing register view ---
@api_view(['POST'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])       
def register(request):
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

    if requested_role == 'customer' and not (user.role == 'dietitian' or user.is_admin or user.is_superadmin):
        return Response({'error': 'You do not have permission to create customer accounts.'}, status=status.HTTP_403_FORBIDDEN)
    # --- End Authorization Logic ---

    user_serializer = AccountSerializer(data=data, context={'request': request})

    if user_serializer.is_valid():
        if not Account.objects.filter(email=user_serializer.validated_data['email']).exists():
            user = user_serializer.save()
            # Optionally send a welcome email or first-time login instructions here
            return Response({'message': f'{requested_role.capitalize()} account registered successfully. Please use forgot password to set your actual password.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': f'Account with email {data["email"]} already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Existing user_profile view ---
@api_view(['GET', 'PATCH']) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
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


@api_view(['GET'])
def get_user_profile_name_by_id(request):
    profile_id = request.query_params.get('id') 
    if not profile_id:
        return Response(
            {'error': 'The "profile_id" query parameter is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )    
    try:
        profile_id = int(profile_id)
    except ValueError:
        return Response(
            {'error': 'Invalid "profile_id" format. Must be an integer.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user_profile = Account.objects.get(id=profile_id)
        return Response({"name": user_profile.username, "gender": user_profile.gender, "last_visit": user_profile.last_login}, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e: 
        return Response({"detail": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# --- Existing login_view ---
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:  # Check if the user's account is active
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
                return Response({'error': 'Please verify your email or reset password to activate your account.'}, status=status.HTTP_403_FORBIDDEN) # Modified message
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Existing list_accounts view ---
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_accounts(request):
    user = request.user
    accounts = Account.objects.all()

    if user.is_superadmin or user.is_admin:
        dietician_id_param = request.query_params.get('dietician_id', None)
        if dietician_id_param:
            try:
                dietician_id_param = int(dietician_id_param)
                accounts = accounts.filter(dietician_id=dietician_id_param)
                count = accounts.count()
            except ValueError:
                return Response({'error': 'Invalid dietician_id provided. Must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
    elif user.role == 'dietitian':
        accounts = accounts.filter(dietician_id=user.id)
        count = accounts.count()
    else:
        return Response({'error': 'You do not have permission to view accounts.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = AccountSerializer(accounts, many=True)
    return Response({"total_accounts": count, "results": serializer.data}, status=status.HTTP_200_OK)


# --- NEW: Request Password Reset OTP API ---
@api_view(['POST'])
def request_password_reset_otp(request):
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


# --- NEW: Verify OTP API ---
@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        # OTP is valid and not expired, and user exists
        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- NEW: Reset Password Confirm API ---
@api_view(['POST'])
def reset_password_confirm(request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() # This method also marks OTP as used
        return Response({'message': 'Password reset successfully. You can now log in with your new password.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)