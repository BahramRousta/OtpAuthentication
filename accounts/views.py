from django.contrib.auth import get_user_model, login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from .throttling import GetOTPRateThrottle, LoginRateThrottle
from .models import Otp, CustomUser
from accounts.serializers import (
    OtpRequestSerializer,
    RequestOtpResponseSerializer,
    VerifyOtpRequest,
    ObtainTokenSerializer,
    SignUpByUsernameSerializer,
    LoginSerializer
)
from django.db.models import Q
User = get_user_model()


def _handle_login(otp, request):
    query = User.objects.filter(username=otp['phone_number'])
    if query.exists():
        user = query.first()
    else:
        user = User.objects.create(username=otp['phone_number'])

    refresh = RefreshToken.for_user(user)
    login(request, user=user)
    return ObtainTokenSerializer({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token)
    }).data


class RegisterApiView(APIView):
    permission_classes = ([AllowAny])
    throttle_classes = [GetOTPRateThrottle, LoginRateThrottle]

    def get(self, request):
        serializer = OtpRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            otp = Otp.objects.create(phone_number=data['input_data'])
            # call SMS web service to send otp code
            print(otp.code)
            return Response(data=RequestOtpResponseSerializer(otp).data)
        else:
            return Response(data=serializer.errors)

    def post(self, request):
        serializer = VerifyOtpRequest(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if Otp.objects.is_valid(
                    data['request_id'],
                    data['phone_number'],
                    data['code']
            ):
                return Response(_handle_login(data, request))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LogOut(APIView):
    permission_classes = ([IsAuthenticated])
    throttle_scope = 'logout'

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class DeleteAccount(APIView):
    permission_classes = ([IsAuthenticated])
    throttle_scope = 'delete_account'

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        transition_list = Transition.objects.filter(owner_id=user.id)
        # delete user all transition
        transition_list.delete()
        user.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)


class SignUp(APIView):

    def post(self, request):
        serializer = SignUpByUsernameSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            user = CustomUser.objects.create(username=data["username"])
            user.set_password(data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            login(request, user=user)

            token = ObtainTokenSerializer({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            }).data

            return Response(status=status.HTTP_200_OK, data=token)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LogIn(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            user = CustomUser.objects.filter(Q(username=data["username"]) |
                                              Q(phone_number=data["username"]) |
                                              Q(email=data["username"])).first()
            # print(user)

            if user and user.check_password(data["password"]):
                login(request, user)

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
