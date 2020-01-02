from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def notify_report(sender, **kwargs):
    print('Order here.')
