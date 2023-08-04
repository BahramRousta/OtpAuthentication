import httpx
import pytest
from asgiref.sync import sync_to_async
from django.urls import reverse


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


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_login_user_by_user_password(user):
    async_client = httpx.AsyncClient()
    login_url = "http://127.0.0.1:8000/api-accounts/login/"
    data = dict(username='username', password='user_password')
    # sync_post = sync_to_async(async_client.post)

    response = await async_client.post(login_url, data=data)

    # response = await sync_post(login_url, data)
    #
    print(response)
    # data = response.data
    # #
    # assert response.status_code == 200
    # assert "access_token" in data
    # assert "refresh_token" in data