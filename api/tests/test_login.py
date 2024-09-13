import pytest
from api.models import db, User

def test_login(client, session):
    user = User(username='testuser')
    user.set_password('password123')
    session.add(user)
    session.commit()

    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    data = response.get_json()

    assert response.status_code == 200
    assert 'access_token' in data

    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'access_token' not in response.get_json()
