from src.models.user.models import User


def test_create_user(user):
    print(user)
    assert isinstance(user, User)
