from rest_framework import serializers

from .models import Dish
from .models import Order
from .models import Feedback


class DishSerializer(serializers.ModelsSerializers):

    class Meta:
        model = Dish
        fields = ('id', 'name', 'price', 'date',
                  'description', 'sold_out', 'photo')


class OrderSerializer(serializers.ModelsSerializers):

    class Meta:
        model = Order
        fields = ('id', 'date', 'name', 'id_no', 'contact_no',
                  'dish', 'count', 'amount', 'served')
        depth = 1


class FeedbackSerializer(serializers.ModelsSerializers):

    class Meta:
        model = Feedback
        fields = ('id', 'date', 'contact_no', 'name', 'content')
