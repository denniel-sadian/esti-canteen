from django.views.generic import ListView
from django.utils.timezone import datetime

from .models import Dish


class HomeView(ListView):
    context_object_name = 'dishes'
    template_name = 'canteen/dish-list.html'

    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())