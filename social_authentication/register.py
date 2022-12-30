from django.contrib.auth import authenticate
from accounts.models import CustomUser
import random
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not CustomUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)
    print(filtered_user_by_email)
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            print(filtered_user_by_email[0].email)
            registered_user = authenticate(
                username=filtered_user_by_email[0].username, password=settings.SOCIAL_SECRET)
            print(registered_user)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

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

        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }