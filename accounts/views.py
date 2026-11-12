from django.contrib.auth import authenticate,login,logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from accounts.serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully.'}, status=201)




@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'}, status=200)

    return Response({'error': 'Invalid credentials.'}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful.'}, status=200)


@api_view(['GET'])
def profile_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)