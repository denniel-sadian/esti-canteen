"""
Forms for `canteen`
"""


from django import forms
from django.utils.timezone import datetime

from .models import Dish
from .models import Order


class OrderForm(forms.ModelForm):
    dish = forms.ModelChoiceField(
        queryset=Dish.objects.filter(date=datetime.now())
    )

    class Meta:
        model = Order
        fields = ['name', 'id_no', 'contact_no', 'count', 'dish']
