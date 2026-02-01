from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError

def check_auth(request):
    JWT_authenticator = JWTAuthentication()
    try:
        response = JWT_authenticator.authenticate(request)
    except InvalidToken as ex:
        print(f'ex.detail: {ex.detail}')
        return (False, "Token is invalid or expired")
   
    if response is None:
        return (False, "User is not authenticated")
    
    return (True, None)

def validate_username(username):
    # validate username length
    # validate username only includes letter, numbers, underscore
    if not username.isalnum():
        return False
    
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