"""
Forms for `canteen`
"""


from django import forms
from django.utils.timezone import datetime
from django.db.models import Q

from .models import Dish
from .models import Order


class OrderForm(forms.ModelForm):
    dish = forms.ModelChoiceField(queryset=None)
    contact_no = forms.CharField(min_length=11)

    def __init__(self, *args, **kwargs):
        super().__init__( * args, ** kwargs)
        # Get the dishes
        self.fields['dish'].queryset = Dish.objects.filter(
            Q(date=self.instance.date) | Q(everyday=True))

    class Meta:
        model = Order
        fields = ['name', 'id_no', 'contact_no', 'count', 'dish']
