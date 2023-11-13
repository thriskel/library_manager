# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 15 minutes
"""

from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=50
    )
    surname = models.CharField(
        max_length=50
    )
    birth_date = models.DateField(
        verbose_name='Date of birth',
        null=False,
        blank=False
    )
    death_date = models.DateField(
        null=True,
        blank=True
    )

    def is_alive(self):
        """If the author is alive, returns True, False otherwise"""
        return self.death_date is None

    def __str__(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        author_name = f'{self.name} {self.surname}'
        author_longevity = f'({self.birth_date} {self.death_date})'
        return f'Author: ({author_name} {author_longevity})'


class Category(models.Model):
    name = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Category: ({self.name})'


class Book(models.Model):
    title = models.CharField(
        max_length=50
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    published_date = models.DateField(
        verbose_name='Date of publication',
        null=False,
        blank=False
    )

    def is_available(self):
        """
        Returns True if the book is available for lending, False otherwise
        """
        is_available = True
        not_returned = self.booklending_set.filter(return_date=None)

        if not_returned:
            is_available = False

        return is_available

    def __str__(self):
        return f'{self.title} - {self.author}'

    def __repr__(self):
        return f'Book: ({self.title} {self.author} {self.category} {self.published_date})'


class Customer(models.Model):
    name = models.CharField(
        max_length=50
    )
    surname = models.CharField(
        max_length=50
    )
    address = models.CharField(
        max_length=120
    )
    phone_number = models.CharField(
        max_length=50
        )
    email = models.EmailField(
        max_length=100
    )

    def __str__(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        customer_name = f'{self.name} {self.surname}'
        customer_contact = f'({self.address} {self.phone_number} {self.email})'
        return f'Customer: ({customer_name} {customer_contact})'


class BookLending(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    lending_date = models.DateField(
        verbose_name='Date of lending',
        null=False,
        blank=False
    )
    return_date = models.DateField(
        verbose_name='Date of return',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.book} - {self.customer}'

    def __repr__(self):
        return f'Book lending: ({self.book} {self.customer} {self.lending_date} {self.return_date})'
