import pytest


@pytest.mark.django_db
def test_login_by_username_password(user, client):

    response = client.post("/api-accounts/login/", dict(username="username", password="user_password"))

    data = response.data

    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.django_db
def test_login_user_fail(client):
    payload = dict(
        username="username",
        password="user_password"
    )

    response = client.post("/api-accounts/login/", payload)

    assert response.status_code == 403

