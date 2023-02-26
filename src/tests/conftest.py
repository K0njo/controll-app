import pytest

from src.models.user.models import User


@pytest.fixture(autouse=True)
def user():
    user = User()
    user.id = 111
    user.username = "test"
    user.password = "test"
    user.first_name = "test"
    user.last_name = "test"
    user.email = "test"
    user.hash_password = "test"
    user.is_active = True

    return user
