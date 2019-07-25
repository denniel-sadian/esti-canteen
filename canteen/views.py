from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils.timezone import datetime

from .models import Dish


class HomeView(ListView):
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())


class DishView(DetailView):
    model = Dish