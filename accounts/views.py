from django.shortcuts import render


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from urllib.parse import urljoin
import requests


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

class GoogleCodeExchangeView(APIView):
    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "Missing authorization code"}, status=400)

        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }

        token_url = "https://oauth2.googleapis.com/token"
        response = requests.post(token_url, data=data)
        print(response.json()) 
        if response.status_code != 200:
            return Response(response.json(), status=response.status_code)

        return Response(response.json())
