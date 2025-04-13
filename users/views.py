from django.shortcuts import render
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
import os
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.conf import settings
from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Client as BaseOAuth2Client,
)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class PatchedGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, response=None, **kwargs):
        # Handle if response is a string (which is what dj-rest-auth does with id_token)
        if isinstance(response, str):
            response = {"id_token": response}
        return super().complete_login(request, app, token, response=response, **kwargs)


class FixedGoogleOAuth2Client(BaseOAuth2Client):
    def __init__(self, *args, **kwargs):
        kwargs.pop("scope_delimiter", None)  # Remove if passed twice
        super().__init__(*args, **kwargs)


class GoogleLogin(SocialLoginView):
    adapter_class = PatchedGoogleOAuth2Adapter
    callback_url = os.environ.get("GOOGLE_OAUTH_CALLBACK_URL")
    client_class = FixedGoogleOAuth2Client


class GoogleExchangeCodeView(APIView):
    permission_classes = [] 

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Code is required'}, status=400)

        # Exchange code for tokens
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            return Response({
                'error': 'Failed to exchange code',
                'details': response.json()
            }, status=400)

        tokens = response.json()
        print("code", code)
        print("hi: ", tokens)
        return Response({
            'access_token': tokens.get('access_token'),
            'id_token': tokens.get('id_token')
        })
