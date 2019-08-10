from rest_framework import serializers

from .models import Dish
from .models import Order
from .models import Feedback


class Dish(serializers.ModelsSerializers):

    class Meta:
        model = Dish
        fields = ('id', 'name', 'price', 'date',
                  'description', 'sold_out', 'photo')
