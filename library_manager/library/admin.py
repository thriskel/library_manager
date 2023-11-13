# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 1 minutes
"""

from django.contrib import admin
from .models import Author, Book, BookLending, Customer, Category

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookLending)
admin.site.register(Customer)
admin.site.register(Category)
