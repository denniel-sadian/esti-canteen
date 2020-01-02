from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Order
from .models import Feedback

channel_layer = get_channel_layer()


def send():
    async_to_sync(channel_layer.group_send)(
        "report", {
            "type": "message",
            'message': ''
        }
    )


@receiver(post_save, sender=Order)
def notify_report(sender, **kwargs):
    send()


@receiver(post_delete, sender=Order)
def notify_report_on_delete(sender, **kwargs):
    send()


@receiver(post_save, sender=Feedback)
def notify_feedbacks(sender, **kwargs):
    send()
