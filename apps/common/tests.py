import pytest
from django.contrib.auth import get_user_model

from tests.factories.user import UserFactory

User = get_user_model()

@pytest.mark.django_db
def test_user_list(client, new_user):
    """client is only necessary for sending test request, with client.get(), post(), put(), patch()"""
    assert User.objects.count() == 1
    assert User.objects.first().email == new_user.email
    assert User.objects.first().username == new_user.username


@pytest.mark.django_db
def test_user_list_with_manual_created_user(client):
    """Factory will generate random values if not provided"""
    new_user = UserFactory(email="samandarkhodjiyev@gmail.com", username="strong_password")

    assert User.objects.count() == 1
    assert User.objects.first().email == new_user.email
    assert User.objects.first().username == new_user.username
