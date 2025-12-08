from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError

def is_authenticated(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)

    return response is None

def validate_username(username):
    # validate username length
    # validate username only includes letter, numbers, underscore
    
    return True

def validate_password(password):
    # validate password length
    # validate password only includes letters, numbers, certain special characters ...

    return True

def validate_email(email):
    try:
        django_validate_email(email)
    except ValidationError:
        return False
       
    return True