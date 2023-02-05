from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
import random
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from accounts.serializers import ObtainTokenSerializer


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not CustomUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                username=filtered_user_by_email[0].username, password=settings.SOCIAL_SECRET)

            refresh = RefreshToken.for_user(registered_user)
            return ObtainTokenSerializer({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            }).data

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name),
            'email': email,
            'password': settings.SOCIAL_SECRET}

        user = CustomUser.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            username=user.username, password=settings.SOCIAL_SECRET)

        refresh = RefreshToken.for_user(new_user)
        return ObtainTokenSerializer({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }).data