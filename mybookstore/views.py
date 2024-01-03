from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserCreationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class MobileNumberLoginView(APIView):
    def post(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number')

        user = authenticate(request, mobile_number=mobile_number)

        if user is not None:
            login(request, user)
            token = self.get_or_create_token(user)
            print(f"Token: {token}")
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Please enter your details.'}, status=status.HTTP_401_UNAUTHORIZED)

    # def post(self, request, *args, **kwargs):
    #     mobile_number = request.data.get('mobile_number')

    #     try:
    #         user = CustomUser.objects.get(mobile_number=mobile_number)
    #         token = self.get_or_create_token(user)
    #         print(f"Token: {token}")
    #         return Response({'token': token}, status=status.HTTP_200_OK)

    #     except CustomUser.DoesNotExist:
    #         # Mobile number not found, prompt user to enter details
    #         return Response({'detail': 'Mobile number not found. Please enter your details.'}, status=status.HTTP_404_NOT_FOUND)

    def get_or_create_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserCreationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token = MobileNumberLoginView().get_or_create_token(user)
            print(f"Token: {token}")
            return Response({'token': token}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request, *args, **kwargs):
    #     serializer = CustomUserCreationSerializer(data=request.data)

    #     if serializer.is_valid():
    #         user = serializer.save()
    #         token = MobileNumberLoginView().get_or_create_token(user)
    #         print(f"Token: {token}")
    #         return Response({'token': token}, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
    # permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     try:
    #         print(f"request.data.get('refresh_token'): {request.data.get('refresh_token')}")
    #         refresh_token = request.data.get('refresh_token')
    #         if refresh_token:
    #             RefreshToken(refresh_token).blacklist()
    #             return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
