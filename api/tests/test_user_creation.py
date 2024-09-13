import pytest
from api.models import db, User
from api.user_service import create_user

def test_create_user(session):
    user = create_user('newuser', 'password123')
    assert user.username == 'newuser'
    assert user.check_password('password123') is True

    with pytest.raises(ValueError):
        create_user('newuser', 'password123')
