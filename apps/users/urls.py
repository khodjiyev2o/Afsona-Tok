from django.urls import path

from apps.users.api_endpoints import *
from apps.users.api_endpoints.LoginConfirm.views import LoginConfirmAPIView

app_name = 'users'

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name='login'),
    path("login/confirm", LoginConfirmAPIView.as_view(), name='login_confirm')
]