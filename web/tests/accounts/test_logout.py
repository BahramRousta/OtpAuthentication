def test_logout(db, user, client):

    response = client.post("/api-accounts/login/", dict(username="username", password="user_password"))

    data = response.data

    payload = dict(
        refresh_token=data["refresh_token"]
    )

    client.credentials(HTTP_AUTHORIZATION="Bearer " + data["access_token"])

    response = client.post("/api-accounts/logout/", payload)

    assert response.status_code == 205

