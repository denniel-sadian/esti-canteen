"""
Forms for `canteen`
"""


from django import forms
from django.utils.timezone import datetime

from .models import Dish
from .models import Order


class OrderForm(forms.ModelForm):
    dish = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__( * args, ** kwargs)
        self.fields['dish'].queryset = Dish.objects.filter(date=self.instance.date)

    class Meta:
        model = Order
        fields = ['name', 'id_no', 'contact_no', 'count', 'dish']
