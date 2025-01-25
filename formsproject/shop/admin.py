from django.contrib import admin
from .models import Products, Category

admin.site.register(Products)  # Register the Product model
admin.site.register(Category)