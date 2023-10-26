from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from api.serializers.serializers_barber import CustomTokenObtainPairSerializer, GetUserSerializer, UserSerializer
User = get_user_model()


class UserLoginView(TokenObtainPairView):
    """
    View to handle login
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class UserRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Barber.
    """
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({'message': 'User registered successfully.'})
    

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class GetAllBarbers(generics.ListAPIView):
    serializer_class = GetUserSerializer
    
    def get_queryset(self):
        return User.objects.get_barbers()