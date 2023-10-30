from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_barber', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, '', password, **extra_fields)
    
    def get_active_users(self):
        return self.filter(is_active=True)
    
    def get_barbers(self):
        return self.filter(is_barber=True)
    
    def get_staff_users(self):
        return self.filter(is_staff=True)
    
    def get_superuser(self):
        return self.get(is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=False, default='sanja')
    # phone = models.CharField(max_length=100, blank=False)
    # avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_barber = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.name


    # def get_avatar(self):
    #     if self.avatar:
    #         return settings.WEBSITE_URL + self.avatar.url
    #     else:
    #         return 'https://picsum.photos/200/200'
