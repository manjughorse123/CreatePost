import jwt
from django.conf import settings
from datetime import datetime ,timedelta


def generate_access_token(user):

    access_token_payload = {
        'user_name': user.username,
        'user_password': user.password,
        
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token