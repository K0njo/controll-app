from src.models.user.user_model import User


def test_create_user(user):
    print(user)
    assert isinstance(user, User)
