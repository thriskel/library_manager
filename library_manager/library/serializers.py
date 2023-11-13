# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 2 minutes
"""

from library_users.models import User

from rest_framework import serializers

from .models import Author, Category, Book, Customer, BookLending


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for the library app
    """
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """
    Author serializer for the library app
    """
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer for the library app
    """
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """
    Book serializer for the library app
    """

    available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'category', 'published_date', 'available')

    def get_available(self, obj):
        """
        Returns if the book is available or not
        """
        return obj.is_available()


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer serializer for the library app
    """
    class Meta:
        model = Customer
        fields = '__all__'


class BookLendingSerializer(serializers.ModelSerializer):
    """
    BookLending serializer for the library app
    """
    class Meta:
        model = BookLending
        fields = '__all__'
