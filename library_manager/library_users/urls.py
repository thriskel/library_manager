# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 5 minutes
"""

from django.urls import path
from .views import (
    register,
    token,
    refresh_token,
    revoke_token,
)


urlpatterns = [
    path('user-register/', register, name='register_user'),
    path('user-token/', token, name='user_token'),
    path('user-token/refresh/', refresh_token, name='user_refresh_token'),
    path('user-token/revoke/', revoke_token, name='user_revoke_token'),
]
