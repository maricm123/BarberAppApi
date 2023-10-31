from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Overrides the default TokenObtainPairSerializer to return the role in the token response.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access = refresh.access_token
        data['refresh'] = str(refresh)
        data['access'] = str(access)
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the base User model.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'email',)

        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class GetUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the base User model.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email', ]
