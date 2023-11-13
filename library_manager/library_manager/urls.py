# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 5 minutes
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from oauth2_provider.views.base import AuthorizationView, RevokeTokenView, TokenView
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="Library Management System API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/authorize/', AuthorizationView.as_view(), name="authorize"),
    path('o/token/', TokenView.as_view(), name="token"),
    path('o/revoke_token/', RevokeTokenView.as_view(), name="revoke-token"),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('library.urls')),
    path('', include('library_users.urls')),
]

urlpatterns += staticfiles_urlpatterns()
