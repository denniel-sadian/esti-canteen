from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.core.signals import request_started
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db import close_old_connections
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Dish
from .models import Order
from .models import Feedback

channel_layer = get_channel_layer()


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


@receiver(request_started)
def started_request(**kwargs):
    close_old_connections()


@receiver(request_finished)
def finished_request(**kwargs):
    close_old_connections()