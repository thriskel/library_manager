# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 1 hour
"""

from datetime import date

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from library.models import Author, Book, Customer, BookLending
from library.serializers import (AuthorSerializer, BookSerializer,
                                  CustomerSerializer, BookLendingSerializer)


class AuthorList(generics.ListCreateAPIView):
    """
    API view for listing and creating authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @swagger_auto_schema(
        operation_description="List of authors",
        responses={
            200: openapi.Response(
                description="List of authors",
                schema=AuthorSerializer(many=True)
            ),
            401: "Unauthorized"
        },
        tags=['authors']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def destroy(self, request, *args, **kwargs):
        """
        Overriding the perform_destroy method to make validations
        """
        instance = self.get_object()

        author_books_borrowed = BookLending.objects.filter(
            book__author=instance,
            return_date=None
        )

        if author_books_borrowed:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            raise ValidationError(f'Author {instance} has books borrowed')

        super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Retrieve an author",
        responses={
            200: openapi.Response(
                description="Retrieve an author",
                schema=AuthorSerializer()
            ),
            401: "Unauthorized",
            404: "Not found"
        },
        tags=['authors']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an author",
        responses={
            200: openapi.Response(
                description="Update an author",
                schema=AuthorSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Overriding the put method to add swagger documentation
        """
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an author",
        responses={
            200: openapi.Response(
                description="Update an author",
                schema=AuthorSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Overriding the patch method to add swagger documentation
        """
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an author",
        responses={
            204: "No content",
            401: "Unauthorized"
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Overriding the delete method to add swagger documentation
        """
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create an author",
        responses={
            201: openapi.Response(
                description="Create an author",
                schema=AuthorSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Overriding the post method to add swagger documentation
        """
        return super().post(request, *args, **kwargs)


class CustomerList(generics.ListCreateAPIView):
    """
    API view for listing and creating customers
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @swagger_auto_schema(
        operation_description="List of customers",
        responses={
            200: openapi.Response(
                description="List of customers",
                schema=CustomerSerializer(many=True)
            ),
            401: "Unauthorized"
        },
        tags=['customers']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting customers
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def destroy(self, request, *args, **kwargs):
        """
        Overriding the perform_destroy method to make validations
        """
        instance = self.get_object()

        customer_books_borrowed = instance.booklending_set.filter(
            return_date=None
        )

        if customer_books_borrowed:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            raise ValidationError(f'Customer {instance} has books borrowed')

        super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Retrieve a customer",
        responses={
            200: openapi.Response(
                description="Retrieve a customer",
                schema=CustomerSerializer()
            ),
            401: "Unauthorized",
            404: "Not found"
        },
        tags=['customers']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a customer",
        responses={
            200: openapi.Response(
                description="Update a customer",
                schema=CustomerSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Overriding the put method to add swagger documentation
        """
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a customer",
        responses={
            200: openapi.Response(
                description="Update a customer",
                schema=CustomerSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Overriding the patch method to add swagger documentation
        """
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a customer",
        responses={
            204: "No content",
            401: "Unauthorized"
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Overriding the delete method to add swagger documentation
        """
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a customer",
        responses={
            201: openapi.Response(
                description="Create a customer",
                schema=CustomerSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Overriding the post method to add swagger documentation
        """
        return super().post(request, *args, **kwargs)


class BookList(generics.ListCreateAPIView):
    """
    API view for listing and creating books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @swagger_auto_schema(
        operation_description="List of books",
        responses={
            200: openapi.Response(
                description="List of books",
                schema=BookSerializer(many=True)
            ),
            401: "Unauthorized"
        },
        tags=['books']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def destroy(self, request, *args, **kwargs):
        """
        Overriding the perform_destroy method to make validations
        """
        instance = self.get_object()

        if not instance.is_available():
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            raise ValidationError('This book is currently borrowed by a customer')

        super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Retrieve a book",
        responses={
            200: openapi.Response(
                description="Retrieve a book",
                schema=BookSerializer()
            ),
            401: "Unauthorized",
            404: "Not found"
        },
        tags=['books']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a book",
        responses={
            200: openapi.Response(
                description="Update a book",
                schema=BookSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Overriding the put method to add swagger documentation
        """
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a book",
        responses={
            200: openapi.Response(
                description="Update a book",
                schema=BookSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Overriding the patch method to add swagger documentation
        """
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a book",
        responses={
            204: "No content",
            401: "Unauthorized"
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Overriding the delete method to add swagger documentation
        """
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a book",
        responses={
            201: openapi.Response(
                description="Create a book",
                schema=BookSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Overriding the post method to add swagger documentation
        """
        return super().post(request, *args, **kwargs)


class BookLendingList(generics.ListAPIView):
    """
    API view for listing book lendings
    """
    queryset = BookLending.objects.all()
    serializer_class = BookLendingSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @swagger_auto_schema(
        operation_description="List of book lendings",
        responses={
            200: openapi.Response(
                description="List of book lendings",
                schema=BookLendingSerializer(many=True)
            ),
            401: "Unauthorized"
        },
        tags=['book lendings']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)


class BookLendingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting book lendings
    """
    queryset = BookLending.objects.all()
    serializer_class = BookLendingSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def create(self, request, *args, **kwargs):
        """
        Overriding the perform_update method to make validations
        """
        book = request.data['book']
        lending_date = request.data['lending_date']
        return_date = request.data['return_date']
        error_text = ''

        if return_date:
            if return_date > date.today():
                error_text = 'Return date must be less than today'
            elif return_date < lending_date:
                error_text = 'Return date must be greater than lending date'
        elif not book.is_available():
            error_text = 'This book is currently borrowed by a customer'

        if error_text:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            raise ValidationError(error_text)

        super().update(request, *args, **kwargs)

        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Overriding the perform_update method to make validations
        """
        instance = self.get_object()
        lending_date = instance.lending_date
        return_date = instance.return_date
        error_text = ''

        if return_date:
            if return_date < lending_date:
                error_text = 'Return date must be greater than lending date'
            if return_date > date.today():
                error_text = 'Return date must be less than today'

        if error_text:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            raise ValidationError(error_text)

        super().update(request, *args, **kwargs)

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Overriding the perform_destroy method to make validations
        """
        instance = self.get_object()

        if not instance.return_date:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            raise ValidationError('The book has not been returned yet')

        super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Retrieve a book lending",
        responses={
            200: openapi.Response(
                description="Retrieve a book lending",
                schema=BookLendingSerializer()
            ),
            401: "Unauthorized",
            404: "Not found"
        },
        tags=['book lendings']
    )
    def get(self, request, *args, **kwargs):
        """
        Overriding the get method to add swagger documentation
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a book lending",
        responses={
            200: openapi.Response(
                description="Update a book lending",
                schema=BookLendingSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Overriding the put method to add swagger documentation
        """
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a book lending",
        responses={
            200: openapi.Response(
                description="Update a book lending",
                schema=BookLendingSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Overriding the patch method to add swagger documentation
        """
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a book lending",
        responses={
            204: "No content",
            401: "Unauthorized"
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Overriding the delete method to add swagger documentation
        """
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a book lending",
        responses={
            201: openapi.Response(
                description="Create a book lending",
                schema=BookLendingSerializer()
            ),
            400: "Bad request",
            401: "Unauthorized"
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Overriding the post method to add swagger documentation
        """
        return super().post(request, *args, **kwargs)
