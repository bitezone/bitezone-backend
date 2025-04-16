from django.urls import path, include, re_path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from dj_rest_auth.urls import LoginView

app_name = "users"

urlpatterns = [
    # path("registration/", include("dj_rest_auth.registration.urls")),
    path("", include("dj_rest_auth.urls")),
    # path("user/", get_current_user, name="user_info"),
    path("authenticate/google/", GoogleLogin.as_view(), name="google_login"),
    path("code/", CodeView, name="codetest"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # path("accounts/", include("allauth.urls")),
]
