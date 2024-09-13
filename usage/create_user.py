from api.models import db, User
from api.user_service import create_user

user = create_user(username='testuser', password='testpassword')

print(f'User created: {user.username}')
