def test_get_refresh_token(db, client, otp):

    payload = dict(
        otp_receiver=f"{otp.otp_receiver}",
        request_id=f"{otp.request_id}",
        code=f"{otp.code}"
    )

    response = client.post("/api-accounts/register/", payload)

    data = response.data

    token = dict(
        refresh=data["refresh_token"]
    )

    res = client.post("/api-accounts/token/refresh/", token)

    assert res.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_get_refresh_token_fail(client):
    payload = [
        dict(refresh="invalid_token"),
        dict(refresh="")
    ]

    for status in payload:

        response = client.post("/api-accounts/token/refresh/", status)

        if status == payload[0]:
            print(payload[0])
            assert response.status_code == 401
        else:
            assert response.status_code == 400