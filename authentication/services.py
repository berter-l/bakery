from re import error

from django.contrib.auth.models import User
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction

from catalog.services import error_exists
from promotions.models import UserBonus


def login_user(data):
    user = authenticate(username=data['name'], password=data['password'])
    if user is not None:
        refresh_token = RefreshToken.for_user(user)
        return 200, {'access_token': str(refresh_token.access_token), 'refresh_token': str(refresh_token)}
    else:

        return 400, {'message': 'User not found'}


def registration(data):
    error = error_exists(data, User, ['password_confirmation'])
    if error:
        return 400, {'message': error}
    else:
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=data['username'], email=data['email'],
                                                password=data['password'])
                refresh_token = RefreshToken.for_user(user)
                return 200, {'access_token': str(refresh_token.access_token), 'refresh_token': str(refresh_token)}
        except:
            return 500, {'message': 'произошла ошибка'}


def update_token(request, token):
    try:
        refresh = RefreshToken(token['refresh_token'])

        new_token = RefreshToken.for_user(request.user)
        refresh.blacklist()
        return 200, {'access_token': str(new_token.access_token), 'refresh_token': str(new_token)}
    except Exception as e:
        return 400, {'message': 'токен не действителен'}


def logout(request, token):
    try:
        refresh = RefreshToken(token)
        refresh.blacklist()
        return 200, {'access_token': 'logout'}
    except Exception as e:
        return 400, {'message': 'токен не действителен'}


def get_profile(request):
    data = UserBonus.objects.filter(user=request.user).select_related('user').first()
    if data is not None:
        return 200, {
            'username': data.user.username,
            'balance': data.balance,
            'email': data.user.email,
        }
    else:
        return 400, {'message': 'User not found'}
