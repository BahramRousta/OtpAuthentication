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


@pytest.fixture
def otp_response_fail(otp, client):
    """
    Return unauthorized response when data is incorrect.
    :param otp:
    :param client:
    :return: apiclient response
    """
    counter = 0
    payload = [
        dict(otp_receiver=f"bahramrousta@gmail.com", request_id=f"{otp.request_id}", code=f"{otp.code}"),
        dict(otp_receiver=f"{otp.otp_receiver}", request_id="6180b2ec-4280-4cd3-98d4-0859829ea194", code=f"{otp.code}"),
        dict(otp_receiver=f"{otp.otp_receiver}", request_id=f"{otp.request_id}", code=f"124345"),
    ]

    response = None
    for status in payload:
        counter += 1
        response = client.post("/api-accounts/register/", status)

    return response

