import pytest
from pytest_factoryboy import register

from tests.factories import UserFactory

register(UserFactory)

@pytest.fixture()
def new_user(db, user_factory):
    return user_factory.create()
