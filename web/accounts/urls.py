from django.urls import path
from .views import (
    RegisterApiView,
    LogOut,
    DeleteAccount,
    SignUp,
    LogIn,
    LogoutAllView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
    path('delete_account/', DeleteAccount.as_view(), name='delete_account'),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]