# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 20 minutes
"""

from datetime import date

from django.test import TestCase
from django.urls import reverse

from library.models import Author, Book, Category, Customer, BookLending

from rest_framework import status
from rest_framework.test import APITestCase


class AuthorTests(TestCase):
    """
    Test module for Author model
    """
    def setUp(self):
        self.author_1 = Author.objects.create(
            name='Author 1',
            surname='Surname 1',
            birth_date=date(2023, 1, 1),
            death_date=date(2023, 1, 2),
        )
        self.author_2 = Author.objects.create(
            name='Author 2',
            surname='Surname 2',
            birth_date=date(2023, 1, 1),
            death_date=None
        )

    def test_author_is_alive(self):
        self.assertEqual(
            self.author_1.is_alive(), False)
        self.assertEqual(
            self.author_2.is_alive(), True)


class BookTests(TestCase):
    """
    Test module for Book model
    """
    def setUp(self):
        self.author = Author.objects.create(
            name='Author 1',
            surname='Surname 1',
            birth_date=date(2023, 1, 1),
            death_date=date(2023, 1, 2)
        )
        category = Category.objects.create(
            name='Aventuras'
        )
        self.book_1 = Book.objects.create(
            title='Book 1',
            author=self.author,
            category=category,
            published_date=date(2023, 1, 1)
        )
        self.book_2 = Book.objects.create(
            title='Book 2',
            author=self.author,
            category=category,
            published_date=date(2023, 1, 1)
        )

    def test_book_is_available(self):
        self.assertEqual(
            self.book_1.is_available(), True)
        self.assertEqual(
            self.book_2.is_available(), True)


class AuthorDetailTestCase(APITestCase):
    """
    Test module for AuthorDetail view
    """
    def setUp(self):
        self.author = Author.objects.create(
            name='Author 1',
            surname='Surname 1',
            birth_date=date(2023, 1, 1),
            death_date=date(2023, 1, 2)
        )
        self.url = reverse('author-detail' , args=(self.author.id,))

    def test_get_author(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_author(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_author_with_borrowed_books(self):
        category = Category.objects.create(
            name='Aventuras'
        )
        book = Book.objects.create(
            title='Book 1',
            author=self.author,
            category=category,
            published_date=date(2023, 1, 1)
        )
        customer = Customer.objects.create(
            name='Customer 1',
            surname='Surname 1',
            address='Address 1',
            phone_number='111111111',
            email='asda@asda.com',
        )
        BookLending.objects.create(
            book=book,
            customer=customer,
            lending_date=date(2023, 1, 1)
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_author(self):
        data = {
            'name': 'Author 1',
            'surname': 'Surname 1',
            'birth_date': '2023-01-01',
            'death_date': '2023-01-01'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDetailTestCase(APITestCase):
    """
    Test module for BookDetail view
    """
    def setUp(self):
        self.author = Author.objects.create(
            name='Author 1',
            surname='Surname 1',
            birth_date=date(2023, 1, 1),
            death_date=date(2023, 1, 2)
        )
        category = Category.objects.create(
            name='Aventuras'
        )
        self.book = Book.objects.create(
            title='Book 1',
            author=self.author,
            category=category,
            published_date=date(2023, 1, 1)
        )
        self.url = reverse('book-detail' , args=(self.book.id,))

    def test_get_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_book(self):
        data = {
            'title': 'Book 1',
            'author': self.author.id,
            'category': self.book.category.id,
            'published_date': '2023-01-01'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_with_borrowed_books(self):
        customer = Customer.objects.create(
            name='Customer 1',
            surname='Surname 1',
            address='Address 1',
            phone_number='111111111',
        )
        BookLending.objects.create(
            book=self.book,
            customer=customer,
            lending_date=date(2023, 1, 1)
        )


class CustomerDetailTestCase(APITestCase):
    """
    Test module for CustomerDetail view
    """
    def setUp(self):
        self.customer = Customer.objects.create(
            name='Customer 1',
            surname='Surname 1',
            address='Address 1',
            phone_number='111111111',
        )
        self.url = reverse('customer-detail' , args=(self.customer.id,))

    def test_get_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_customer(self):
        data = {
            'name': 'Customer 1',
            'surname': 'Surname 1',
            'address': 'Address 1',
            'phone_number': '111111111',
            'email': 'prueba@prueba.es'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_customer(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_customer_with_borrowed_books(self):
        author = Author.objects.create(
            name='Author 1',
            surname='Surname 1',
            birth_date=date(2023, 1, 1),
            death_date=date(2023, 1, 2)
        )
        category = Category.objects.create(
            name='Aventuras'
        )
        book = Book.objects.create(
            title='Book 1',
            author=author,
            category=category,
            published_date=date(2023, 1, 1)
        )
        BookLending.objects.create(
            book=book,
            customer=self.customer,
            lending_date=date(2023, 1, 1),
            return_date=None
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookLendingDetailTestCase(APITestCase):
    """
    Test module for BookLendingDetail view
    """
    def setUp(self):
        self.author = Author.objects.create(
            name='Author 1',
            surname='Surname 1',
            birth_date=date(2023, 1, 1),
            death_date=date(2023, 1, 2)
        )
        category = Category.objects.create(
            name='Aventuras'
        )
        self.book = Book.objects.create(
            title='Book 1',
            author=self.author,
            category=category,
            published_date=date(2023, 1, 1)
        )
        self.customer = Customer.objects.create(
            name='Customer 1',
            surname='Surname 1',
            address='Address 1',
            phone_number='111111111',
        )
        self.book_lending = BookLending.objects.create(
            book=self.book,
            customer=self.customer,
            lending_date=date(2023, 1, 1)
        )
        self.url = reverse('lending-detail' , args=(self.book_lending.id,))

    def test_get_book_lending(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_book_lending(self):
        data = {
            'book': self.book.id,
            'customer': self.customer.id,
            'lending_date': '2023-01-01',
            'return_date': '2023-01-01'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_lending_with_return_date_none(self):
        self.book_lending.return_date = None
        self.book_lending.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_book_lending_with_return_date(self):
        self.book_lending.return_date = date(2023, 1, 1)
        self.book_lending.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
