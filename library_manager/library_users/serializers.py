# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 1 minutes
"""

from library_users.models import User

from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Register user serializer for the library app
    """
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
