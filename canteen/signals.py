from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Order

channel_layer = get_channel_layer()


@receiver(post_save, sender=Order)
def notify_report(sender, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "report", {
            "type": "message",
            'message': ''
        }
    )
