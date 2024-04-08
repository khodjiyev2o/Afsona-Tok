from django.urls import path

from apps.users.api_endpoints import *

app_name = 'users'

urlpatterns = [
    path("login/", LoginSendSMSView.as_view(), name='login'),
    path("login/confirm/", LoginConfirmView.as_view(), name='login_confirm'),
    path("profile-update/", ProfileUpdateView.as_view(), name='profile_update'),
    path("profile-detail/", ProfileDetailView.as_view(), name='profile_detail'),
]
