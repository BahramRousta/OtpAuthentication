import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser, Otp


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='username', password='user_password')


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def otp():
    return Otp.objects.create(otp_receiver="bahramrousta1991@gmail.com")