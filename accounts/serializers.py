import re
from rest_framework import serializers
from .models import Otp, CustomUser
from .utils import PHONE_PAtTERN_REGEX, MAIL_PATTERN_REGEX

class OtpRequestSerializer(serializers.Serializer):
    """
        get user phone number for create an otp
    """
    otp_receiver = serializers.CharField(allow_null=False, required=True)

    def validate(self, data):
        otp_receiver = data["otp_receiver"]

        # phone_number_re = re.compile(PHONE_PAtTERN_REGEX)
        # email_re = re.compile(MAIL_PATTERN_REGEX)

        if re.fullmatch(PHONE_PAtTERN_REGEX, otp_receiver) or re.fullmatch(MAIL_PATTERN_REGEX, otp_receiver):
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
        fields = ['request_id', 'otp_receiver', 'code']
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
