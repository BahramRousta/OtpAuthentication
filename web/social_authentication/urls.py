from django.urls import path

from .views import GoogleSocialAuthView

urlpatterns = [
    path('google-auth/', GoogleSocialAuthView.as_view()),
]
