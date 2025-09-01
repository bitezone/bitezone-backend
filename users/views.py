from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.utils.dateparse import parse_datetime

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from menu.models import Menus

from .models import MealSession
from .serializers import MealSessionSerializer

import requests
import urllib
import os

from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  # This is fix for incompatibility between django-allauth==65.3.1 and dj-rest-auth==7.0.1
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class GoogleLogin(SocialLoginView):
    # class GoogleAdapter(GoogleOAuth2Adapter):
    #     access_token_url = "https://oauth2.googleapis.com/token"
    #     authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
    #     profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get("GOOGLE_OAUTH_CALLBACK_URL")
    client_class = CustomGoogleOAuth2Client


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def CodeView(request):

    if request.method == "GET":
        code = urllib.parse.unquote(request.query_params["code"])

        token_endpoint_url = os.environ.get("BACKEND_URL") + "/users/code"
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(
            {
                "code": code,
                "curl": f"curl -H 'code {code}' {token_endpoint_url}/users/authenticate/google/",
            }
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def UserLogOutView(request: Request):
    print("request", request.data)
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"detail": "Successfully logged out."})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


class MealSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = MealSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        queryset = MealSession.objects.filter(user=user)

        date_str = self.request.query_params.get("date", None)

        if date_str:
            parsed_date = parse_datetime(date_str)
            if not parsed_date:
                raise ValidationError(
                    {
                        "error": "Invalid date format. Use ISO 8601 format: 'YYYY-MM-DDTHH:MM:SSZ'"
                    }
                )
            queryset = queryset.filter(date=parsed_date.date())

        return queryset.order_by("-date", "-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
