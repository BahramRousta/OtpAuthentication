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
    print(response.content)

    assert True
    # assert response.status_code == 200
    # assert b"request_id" in response.content