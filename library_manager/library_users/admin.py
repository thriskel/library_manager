# -*- coding: utf-8 -*-
"""
Author: Manuel Martinez
github: @thriskel
time taken: 1 minutes
"""

from django.contrib import admin

from library_users.models import User

admin.site.register(User)
