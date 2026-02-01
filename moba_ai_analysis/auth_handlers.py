from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, ExpiredTokenError
from http import HTTPStatus
import json
from .utils import validate_username, validate_password, validate_email

@require_http_methods(["POST"])
def user_signup(request):
    data = json.loads(request.body)

    if not validate_username(data['username']):
        return JsonResponse({'message':'Username is invalid'}, status=HTTPStatus.BAD_REQUEST) 
    
    if not validate_password(data['password']):
        return JsonResponse({'message':'Password is invalid'}, status=HTTPStatus.BAD_REQUEST) 
    
    if not validate_email(data['email']):
        return JsonResponse({'message':'Email is invalid'}, status=HTTPStatus.BAD_REQUEST) 
    
    if User.objects.filter(username=data['username']).exists():
        return JsonResponse({'message':'Username is already used'}, status=HTTPStatus.BAD_REQUEST) 

    User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
    
    return JsonResponse({'message':'Signed up successfully'}, status=HTTPStatus.OK)

@require_http_methods(["GET"])
def csrf_token(request):
    return JsonResponse({'token': get_token(request)}, status=HTTPStatus.OK)

@require_http_methods(["POST"])
def user_login(request):
    data = json.loads(request.body)
    print(data)

    # username & password precheck
    if not validate_username(data['username']):
        return JsonResponse({'message':'Username is invalid'}, status=HTTPStatus.BAD_REQUEST) 
    

    user = authenticate(request, username=data['username'], password=data['password'])
    print(user)
    
    # print(user)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        print(refresh)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message':'Username or password is invalid'}, status=HTTPStatus.BAD_REQUEST)

@require_http_methods(["POST"])
def user_logout(request):
    data = json.loads(request.body)

    try:
        token = RefreshToken(data['refresh'])
        token.blacklist()
    except ExpiredTokenError:
        return JsonResponse({'message':'Token is expired'}, status=HTTPStatus.UNAUTHORIZED)
    except TokenError:
        return JsonResponse({'message':'Token is invalid'}, status=HTTPStatus.UNAUTHORIZED)
        
    return JsonResponse({'message':'Logged out successfully'}, status=HTTPStatus.OK)

def password_reset(request):
    pass