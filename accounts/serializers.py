import re
from rest_framework import serializers
from .models import Otp, CustomUser


class OtpRequestSerializer(serializers.Serializer):
    """
        get user phone number for create an otp
    """
    input_data = serializers.CharField(allow_null=False, required=True)

    def validate(self, data):
        input_data = data["input_data"]

        phone_number_re = re.compile(r"09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}")
        email_re = re.compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        if re.fullmatch(phone_number_re, input_data) or re.fullmatch(email_re, input_data):
            return data
        raise serializers.ValidationError("Input must be contain email or phone number")


class RequestOtpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['request_id']


class VerifyOtpRequest(serializers.ModelSerializer):
    request_id = serializers.UUIDField(allow_null=False)

    class Meta:
        model = Otp
        fields = ['request_id', 'phone_number', 'code']
        extra_kwargs = {'code': {'required': True}}


class ObtainTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255)
    refresh_token = serializers.CharField(max_length=255)


class SignUpByUsernameSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {'username': {'required': True}}


class LoginSerializer(serializers.Serializer):
    # A username can also contain the user's phone number and email
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
