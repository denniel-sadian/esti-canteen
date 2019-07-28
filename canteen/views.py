from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

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


class RealTimeOrdersView(LoginRequiredMixin, TemplateView):
    login_url = '/admin/login/'
    redirect_field_name = 'next'
    template_name = 'canteen/real_time_orders.html'


def json_orders(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    orders = [
        {
            'id': order.id,
            'name': order.name,
            'id_no': order.id_no,
            'contact_no': order.contact_no,
            'date': order.date,
            'dish': {
                'name': order.dish.name,
                'id': order.dish.id,
                'price': order.dish.price
            },
            'count': order.count,
            'amount': order.amount,
            'served': order.served
        }
        for order in Order.objects.filter(
            date__lt=datetime.now()).order_by('-date')
    ]
    return JsonResponse(orders, safe=False)


def json_report(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    orders = Order.objects.filter(date__lt=datetime.now())
    data = {
        'total_orders_amount':
            orders.aggregate(Sum('amount'))['amount__sum'],
        'total_orders_served_amount':
            orders.filter(served=True).aggregate(Sum('amount'))['amount__sum']
    }
    data['total_amount_still_out'] = (
        data['total_orders_amount'] - data['total_orders_served_amount'])
    return JsonResponse(data)


def api_mark_order_served(request, id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    order = Order.objects.get(id=id)
    order.served = not order.served
    order.save()
    return HttpResponse('Marked as served')


def api_delete_order(request, id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    Order.objects.get(id=id).delete()
    return HttpResponse('Deleted.')
