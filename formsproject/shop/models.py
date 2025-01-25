from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=253, unique=True)
    desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name


class Products(models.Model):  # Make sure the model name matches
    name = models.CharField(max_length=234)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='upload/', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True)
    stocks = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

