import pytest


def test_get_otp_code_by_email(db, client):
    payload = dict(
        otp_receiver="bahramrousta1991@gmail.com"
    )

    response = client.get("/api-accounts/register/", payload)

    assert response.status_code == 200
    assert b"request_id" in response.content


def test_get_otp_code_by_mobile_phone_number(db, client):
    payload = dict(
        otp_receiver="09388791325"
    )

    response = client.get("/api-accounts/register/", payload)

    assert response.status_code == 200
    assert b"request_id" in response.content


def test_otp_login(db, client, otp):

    payload = dict(
        otp_receiver=f"{otp.otp_receiver}",
        request_id=f"{otp.request_id}",
        code=f"{otp.code}"
    )

    response = client.post("/api-accounts/register/", payload)

    data = response.data

    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_otp_login_fail(db, client, otp):

    payload = dict(
        otp_receiver="6180b2ec-4280-4cd3-98d4-0859829ea194",
        request_id=f"{otp.request_id}",
        code=f"{otp.code}"
    )

    response = client.post("/api-accounts/register/", payload)

    assert response.status_code == 401

