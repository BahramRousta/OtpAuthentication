import re
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .throttling import GetOTPRateThrottle, LoginRateThrottle
from .models import Otp, CustomUser
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.serializers import (
    OtpRequestSerializer,
    RequestOtpResponseSerializer,
    VerifyOtpRequest,
    ObtainTokenSerializer,
    SignUpByUsernameSerializer,
    LoginSerializer
)
from .utils import PHONE_PAtTERN_REGEX
from .sms import send_sms

User = get_user_model()


def _handle_login(otp, request):
    query = User.objects.filter(username=otp['otp_receiver'])
    if query.exists():
        user = query.first()
    else:
        user = User.objects.create(username=otp['otp_receiver'])

    refresh = RefreshToken.for_user(user)
    login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
    return ObtainTokenSerializer({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token)
    }).data


class RegisterApiView(APIView):
    """
    Registration with email or mobile number by getting OTP code.
    """

    permission_classes = ([AllowAny])

    throttle_classes = [GetOTPRateThrottle, LoginRateThrottle]

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('otp_receiver',
                                                              in_=openapi.IN_QUERY,
                                                              type=openapi.TYPE_STRING)])
    def get(self, request):
        """
        Get a valid OTP receiver.
        Otp_receiver must be an email or mobile number.
        Return request_id and send otp code to otp_receiver.
        """
        serializer = OtpRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            otp = Otp.objects.create(otp_receiver=data['otp_receiver'])

            if re.fullmatch(PHONE_PAtTERN_REGEX, otp.otp_receiver):
                # call SMS web service to send otp code
                print(otp.code)
                # send_sms(otp=otp.code, mobile_number=otp.otp_receiver)
            else:
                # Send OTP via mail server
                subject = "OTP Code"
                message = f"Your OTP code is {otp.code}.\n" \
                          f"To verify please use this code."
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [data['otp_receiver']]
                send_mail(subject, message, email_from, recipient_list)
                print(otp.code)
            return Response(status=status.HTTP_200_OK, data=RequestOtpResponseSerializer(otp).data)
        else:
            return Response(data=serializer.errors)

    @swagger_auto_schema(request_body=VerifyOtpRequest,
                         responses={'200': 'logged in successfully.'})
    def post(self, request):
        """
        Receives request_id, otp receiver, and an OTP code.
        After validating the input information, the user is logged in.
        Return Refresh and access token.
        """
        serializer = VerifyOtpRequest(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if Otp.objects.is_valid(data['request_id'],
                                    data['otp_receiver'],
                                    data['code']):
                return Response(_handle_login(data, request))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"Message": "Be sure to use current "
                                                                                      "information."})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class SignUp(APIView):
    """
    Sign up with a username and password.
    """

    @swagger_auto_schema(request_body=SignUpByUsernameSerializer)
    def post(self, request):
        """
        Receives a unique username and password then create an account and login after that.
        Return refresh and access tokens.
        """

        serializer = SignUpByUsernameSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            user = CustomUser.objects.create(username=data["username"])
            user.set_password(data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')

            token = ObtainTokenSerializer({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            }).data

            return Response(status=status.HTTP_200_OK, data=token)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LogIn(APIView):
    """
    Users can log in by username, email or mobile number.
    Also, can send email and phone number instead username and login with them.
    """

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        """
        Get username or email or mobile number.
        Return refresh and access tokens.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            user = CustomUser.objects.filter(Q(username=data["username"]) |
                                             Q(phone_number=data["username"]) |
                                             Q(email=data["username"])).first()
            # print(user)

            if user and user.check_password(data["password"]):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                refresh = RefreshToken.for_user(user)
                token = ObtainTokenSerializer({
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }).data
                return Response(status=status.HTTP_200_OK, data=token)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN, data={"Message": "The information is invalid."})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LogOut(APIView):
    """
    Logged out user.
    """
    permission_classes = [IsAuthenticated]
    throttle_scope = 'logout'

    def post(self, request):
        """
        Receives a valid refresh token and sets that into the blacklist to log out the user.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'Bad token': 'Token is expired or invalid.'})


class LogoutAllView(APIView):
    """
    Logged-out user from all device.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'Bad token': 'Token is expired or invalid.'})


class DeleteAccount(APIView):
    """
    Removes account and user information from all models.
    """

    permission_classes = ([IsAuthenticated])
    throttle_scope = 'delete_account'

    def delete(self, request):
        """

        :param request: [http request]
        :return: None
        """
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
