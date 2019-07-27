from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Dish
from .models import Order


class HomeView(ListView):
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())


class DishView(DetailView):
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            date__lt=datetime.now(), dish=self.object).count()
        return context


class OrderView(CreateView):
    model = Order
    fields = ['name', 'id_no', 'count']
    success_url = reverse_lazy('canteen:thanks')

    def form_valid(self, form):
        form.instance.dish = Dish.objects.get(id=self.kwargs['dish'])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(id=self.kwargs['dish'])
        return context


class ThanksView(TemplateView):
    template_name = 'canteen/thanks.html'


def json_orders(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    orders = [
        {
            'name': order.name,
            'id_no': order.id_no,
            'date': order.date,
            'count': order.count,
            'amount': order.amount
        }
        for order in Order.objects.filter(date__lt=datetime.now())
    ]
    return JsonResponse(orders, safe=False)
    