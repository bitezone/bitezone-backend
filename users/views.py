from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
import requests
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
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
    class GoogleAdapter(GoogleOAuth2Adapter):
        access_token_url = "https://oauth2.googleapis.com/token"
        authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    adapter_class = GoogleAdapter
    callback_url = os.environ.get("GOOGLE_OAUTH_CALLBACK_URL")
    client_class = CustomGoogleOAuth2Client


@api_view(["GET"])
@permission_classes([AllowAny])
def CodeView(request):

    if request.method == "GET":
        code = urllib.parse.unquote(request.query_params["code"])

        token_endpoint_url = os.environ.get("BACKEND_URL") + "/users/code"
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(
            {
                "code": code,
                "curl": "curl -H 'code "
                + code
                + "' http://localhost:8000/users/authenticate/google/",
            }
        )
