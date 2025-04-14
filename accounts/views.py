from django.shortcuts import render

# accounts/views.py
from allauth.account.views import ConfirmEmailView
from django.http import HttpResponseRedirect
from django.conf import settings


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)

        redirect_url = settings.FRONTEND_URL + "/login?verified=true"
        return HttpResponseRedirect(redirect_url)
