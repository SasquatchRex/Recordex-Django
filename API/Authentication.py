from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
#
# from .serializers import UserSerializer



@permission_classes([AllowAny])
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)


    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        print(refresh.access_token)
        return Response({
            'access': str(refresh.access_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_login(request):
    return Response({'status': 'User is logged in'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token(request):
    return Response({'status':"User is logged in"},status=status.HTTP_200_OK)