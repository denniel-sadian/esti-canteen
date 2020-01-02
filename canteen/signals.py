from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import channels.layers

from .models import Order

channel_layer = channels.layers.get_channel_layer()


def message(self, event):
    async_to_sync(self.send(text_data=json.dumps({
        'message': ''
    })))


@receiver(post_save, sender=Order)
def notify_report(sender, **kwargs):
    async_to_sync(channel_layer.group_send(
        'report',
        {
            'type': 'message',
            'message': ''
        }
    ))
