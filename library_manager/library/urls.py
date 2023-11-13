# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 1 minute
"""

from django.urls import path

from library.views import (AuthorList, AuthorDetail, BookList, BookDetail,
                    CustomerList, CustomerDetail, BookLendingList, BookLendingDetail)


urlpatterns = [
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('customers/', CustomerList.as_view(), name='customer-list'), 
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('lendings/', BookLendingList.as_view(), name='lending-list'),
    path('lendings/<int:pk>/', BookLendingDetail.as_view(), name='lending-detail')
]
