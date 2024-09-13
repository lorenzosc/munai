from api.models import db, User

def create_user(username, password):
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")
    
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return user

def validate_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None
