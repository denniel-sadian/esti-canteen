"""
Models for the `canteen`
"""

from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import datetime


class Dish(models.Model):
    """
    The Dish model.
    """
    name = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateField()
    description = models.CharField(max_length=101)
    sold_out = models.BooleanField(default=False)
    everyday = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='dishes')

    class Meta:
        verbose_name_plural = 'dishes'
        unique_together = ('name', 'date')

    def __str__(self):
        return self.name


class Feedback(models.Model):
    """
    The Feedback model.
    """
    date = models.DateTimeField(auto_now_add=True)
    contact_no = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f'by {self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class Order(models.Model):
    """
    The order model.
    """
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    id_no = models.CharField('id no.', max_length=100)
    contact_no = models.CharField(max_length=15)
    dish = models.ForeignKey(Dish, related_name='orders', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    amount = models.FloatField(editable=False)
    served = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} orderred {self.dish}'
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.amount = self.count * self.dish.price
        super().save(*args, **kwargs)
