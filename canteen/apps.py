"""
This customized app class is for importing the signals.
"""


from django.apps import AppConfig


class CanteenConfig(AppConfig):
    name = 'canteen'

    def ready(self):
        from . import signals
