import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.models import User

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):
        user = User.objects.all()
        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
            print()
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(username=payload['user_name']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

      
        return (user, None)

    