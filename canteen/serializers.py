from rest_framework import serializers

from .models import Dish
from .models import Order
from .models import Feedback


class DishSerializer(serializers.ModelsSerializers):

    class Meta:
        model = Dish
        fields = ('id', 'name', 'price', 'date',
                  'description', 'sold_out', 'photo')


class FeedbackSerializer(serializers.ModelsSerializers):

    class Meta:
        model = Feedback
        fields = ('date', 'contact_no', 'name', 'content')
