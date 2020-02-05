"""
Models for the `canteen`
"""

from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import datetime

from django_resized import ResizedImageField


# Signal-related imports
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import close_old_connections
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class Dish(models.Model):
    """
    The Dish model.
    """
    name = models.CharField(max_length=50)
    price = models.FloatField()
    date = models.DateField()
    description = models.CharField(max_length=100)
    sold_out = models.BooleanField(default=False)
    everyday = models.BooleanField(default=False)
    photo = ResizedImageField(size=[400, 400], force_format='PNG')

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
    name = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return f'by {self.name}'


class Order(models.Model):
    """
    The order model.
    """
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    id_no = models.CharField('id no.', max_length=20)
    contact_no = models.CharField(max_length=12)
    dish = models.ForeignKey(Dish, related_name='orders', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    served = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} orderred {self.dish}'


# Signal-related functions


def send():
    async_to_sync(channel_layer.group_send)(
        "report", {
            "type": "report",
            'message': ''
        }
    )


@receiver(post_save, sender=Order)
def notify_report(sender, **kwargs):
    send()


@receiver(post_save, sender=Dish)
def notify_dish(sender, **kwargs):
    send()


@receiver(post_delete, sender=Order)
def notify_report_on_delete(sender, **kwargs):
    send()


@receiver(post_save, sender=Feedback)
def notify_feedbacks(sender, **kwargs):
    send()
