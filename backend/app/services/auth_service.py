from datetime import datetime
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.db import users_collection


def register_user(email: str, password: str, name: str) -> dict:
    hashed_password = get_password_hash(password)
    user = {
        'email': email,
        'name': name,
        'hashed_password': hashed_password,
        'created_at': datetime.utcnow(),
        'role': 'user'
    }
    result = users_collection.insert_one(user)
    user['_id'] = str(result.inserted_id)
    return user


def authenticate_user(email: str, password: str) -> dict | None:
    user = users_collection.find_one({'email': email})
    if not user:
        return None
    if not verify_password(password, user['hashed_password']):
        return None
    return user


def create_user_token(user: dict) -> str:
    return create_access_token({'sub': str(user['_id']), 'email': user['email']})
