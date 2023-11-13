# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 8 horas
"""

from datetime import timedelta
import requests

from django.utils import timezone

from oauthlib.common import generate_token
from oauth2_provider.models import (
    get_application_model,
    get_access_token_model,
    get_refresh_token_model,
)
from oauth2_provider.settings import oauth2_settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from library_users.models import User
from library_users.serializers import RegisterUserSerializer


def generate_token_for_user(user, application):
    """
    Generate token for a user using an application
    """
    AccessToken = get_access_token_model()
    RefreshToken = get_refresh_token_model()

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"

    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        expires=expires,
        token=generate_token(),
        scope=scope
    )
    RefreshToken.objects.create(
        user=user,
        application=application,
        token=generate_token(),
        access_token=access_token
    )

    return access_token


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        new_user = serializer.save()

        # create a new application for the user
        Application = get_application_model()
        app = Application(
            name=serializer.data['username'] + '_app',
            user=new_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type='password',
        )
        app.save()

        # generate a token for the user
        user_token = generate_token_for_user(new_user, app)

        data={
            'access_token': user_token.token,
            'refresh_token': user_token.refresh_token.token,
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'token_type': 'Bearer',
            'scope': user_token.scope,
        }

        return Response(data, 200, content_type="application/json")

    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # get the user
    token_user = User.objects.filter(username=request.data['username'])
    if not token_user:
        return Response({'message': 'User not found'}, 400)
    token_user = token_user[0]

    if not token_user.check_password(request.data['password']):
        return Response({'message': 'Wrong credentials'}, 400)

    # get the application
    Application = get_application_model()
    user_app = Application.objects.filter(user=token_user)
    if not user_app:
        user_app = Application(
            name=token_user.username + '_app',
            user=token_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type='password',
        )
        app.save()
    else:
        user_app = user_app[0]

    # check if the user has a token
    AccessToken = get_access_token_model()
    user_token = AccessToken.objects.filter(user=token_user, application=user_app)
    if user_token:
        user_token = user_token[0]
    else:
        user_token = generate_token_for_user(
            token_user, user_app
        )

    data={
        'access_token': user_token.token,
        'refresh_token': user_token.refresh_token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'token_type': 'Bearer',
        'scope': user_token.scope,
    }

    return Response(data, 200, content_type="application/json")


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "refresh_token"}
    '''
    RefreshToken = get_refresh_token_model()

    refresh_token = request.data['refresh_token']
    refresh_token = RefreshToken.objects.filter(token=refresh_token)

    if not refresh_token:
        return Response({'message': 'Invalid refresh token'}, 400)
    refresh_token = refresh_token[0]

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    token = generate_token()

    access_token = refresh_token.access_token
    access_token.token = token
    access_token.expires = expires
    access_token.save()

    data={
        'access_token': access_token.token,
        'refresh_token': access_token.refresh_token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'token_type': 'Bearer',
        'scope': access_token.scope,
    }

    return Response(data, 200, content_type="application/json")


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    AccessToken = get_access_token_model()

    token = request.data['token']

    access_token = AccessToken.objects.filter(token=token)

    if not access_token:
        return Response({'message': 'Invalid token'}, 400)
    access_token = access_token[0]

    access_token.revoke()

    return Response({'message': 'Token revoked'}, 200)
