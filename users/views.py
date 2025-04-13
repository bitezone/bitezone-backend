from django.shortcuts import render
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.conf import settings
import os
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error

# 🔧 Patched Adapter to safely unwrap id_token and validate format
class PatchedGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, response=None, **kwargs):
        # Step 1: Normalize response to dict
        if isinstance(response, str):
            response = {"id_token": response}
        elif isinstance(response, dict):
            pass
        else:
            raise OAuth2Error("Google adapter: response must be string or dict")

        # Step 2: Extract id_token and validate
        id_token = response.get("id_token", "")
        if not isinstance(id_token, str):
            raise OAuth2Error("Google adapter: id_token must be a string")

        if id_token.count(".") != 2:
            print("❌ Received malformed id_token:", id_token)
            raise OAuth2Error("Malformed id_token: not a valid JWT")

        return super().complete_login(request, app, token, response=response, **kwargs)

# 🔧 Fix scope_delimiter error bug
class FixedGoogleOAuth2Client(OAuth2Client):
    def __init__(self, *args, **kwargs):
        kwargs.pop("scope_delimiter", None)
        super().__init__(*args, **kwargs)

# 🔐 View used by frontend to POST access_token + id_token
class GoogleLogin(SocialLoginView):
    adapter_class = PatchedGoogleOAuth2Adapter
    callback_url = os.environ.get("GOOGLE_OAUTH_CALLBACK_URL")
    client_class = FixedGoogleOAuth2Client

# 🔄 Exchanges Google code for tokens
class GoogleExchangeCodeView(APIView):
    permission_classes = []

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "Code is required"}, status=400)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)
        if response.status_code != 200:
            return Response(
                {"error": "Failed to exchange code", "details": response.json()},
                status=400,
            )

        tokens = response.json()
        return Response(
            {
                "access_token": tokens.get("access_token"),
                "id_token": tokens.get("id_token"),
            }
        )
