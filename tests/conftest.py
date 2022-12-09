import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='username', password='user_password')


@pytest.fixture()
def client():
    return APIClient()

