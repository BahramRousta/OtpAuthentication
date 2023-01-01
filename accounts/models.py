import uuid
from datetime import timedelta
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from .utils import generate_otp
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True, null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class OtpManager(models.Manager):

    def is_valid(self, request_id, phone_number, code):
        current_time = timezone.now()
        otp = Otp.objects.filter(request_id=request_id,
                                 otp_receiver=phone_number,
                                 code=code,
                                 created__lt=current_time,
                                 created__gt=current_time - timedelta(seconds=120),
                                 is_active=True).first()

        if otp:
            otp.is_active = False
            otp.save()
        else:
            print('Otp Dose not exist')
        return otp


class Otp(models.Model):
    request_id = models.UUIDField(max_length=36, default=uuid.uuid4)
    otp_receiver = models.CharField(max_length=225, null=False, blank=False)
    code = models.IntegerField(default=generate_otp)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OtpManager()

    def __str__(self):
        return self.otp_receiver
