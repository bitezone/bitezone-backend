from django.urls import path, include,re_path
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('authenticate/google/', GoogleLogin.as_view(), name='google_login'),
    path('users/', include('dj_rest_auth.urls')),
    path('code/', CodeView, name='codetest'),
]