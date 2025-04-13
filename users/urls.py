from django.urls import path, include
from users.views import GoogleLogin, GoogleExchangeCodeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),        
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('auth/google/exchange-code/', GoogleExchangeCodeView.as_view(), name='google_exchange_code'),
]