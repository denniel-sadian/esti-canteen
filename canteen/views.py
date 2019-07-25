from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils.timezone import datetime

from .models import Dish
from .models import Order


class HomeView(ListView):
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())


class DishView(DetailView):
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data( ** kwargs)
        context['orders'] = Order.objects.filter(
            date=datetime.now(), dish=self.object).count()
        return context