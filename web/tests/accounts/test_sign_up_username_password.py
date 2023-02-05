import pytest
from accounts.models import CustomUser


@pytest.mark.django_db
def test_sign_up_by_username_and_password(client):
    payload = dict(
        username="username",
        password="user_password"
    )

    response = client.post("/api-accounts/sign_up/", payload)

    data = response.data

    assert CustomUser.objects.all().count() == 1
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.django_db
def test_sign_up_by_blank_username_and_password(client):
    payload = dict(
        username="",
        password=""
    )

    response = client.post("/api-accounts/sign_up/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_by_duplicated_username_fail(user, client):
    payload = dict(
        username="username",
        password="user_password"
    )

    response = client.post("/api-accounts/sign_up/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_by_without_username_fail(client):
    payload = dict(
        password="user_password"
    )

    response = client.post("/api-accounts/sign_up/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_by_username_without_password_fail(client):
    payload = dict(
        username="username"
    )

    response = client.post("/api-accounts/sign_up/", payload)

    assert response.status_code == 400
