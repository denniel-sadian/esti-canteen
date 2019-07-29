"""
Views for the `canteen`
"""

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
from .models import Feedback


class HomeView(ListView):
    """
    View for listing the dishes at home page.
    """
    context_object_name = 'dishes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_count'] = Order.objects.filter(
            date__date=datetime.now().date()).count()
        return context


    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())


class DishView(DetailView):
    """
    View for displaying the dish's detail.
    """
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            date__date=datetime.now().date(), dish=self.object).count()
        return context


class OrderView(CreateView):
    """
    View for creating orders.
    """
    model = Order
    fields = ['name', 'id_no', 'contact_no', 'count']
    success_url = reverse_lazy('canteen:thanks')

    def form_valid(self, form):
        form.instance.dish = Dish.objects.get(id=self.kwargs['dish'])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(id=self.kwargs['dish'])
        return context


class FeedbackView(CreateView):
    """
    View for creating a feedback.
    """
    model = Feedback
    fields = ['name', 'content']


class ThanksView(TemplateView):
    """
    View for simply thanking the customer.
    """
    template_name = 'canteen/thanks.html'


class RealTimeOrdersView(LoginRequiredMixin, TemplateView):
    """
    View for displaying the template for orders and report.
    """
    login_url = '/admin/login/'
    redirect_field_name = 'next'
    template_name = 'canteen/real_time_orders.html'


def json_orders(request):
    """
    View for displaying all the current orders.
    """
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
            date__date=datetime.now().date()).order_by('-date')
    ]
    return JsonResponse(orders, safe=False)


def json_audit(request):
    """
    View for displaying the audit.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    orders = Order.objects.filter(date__date=datetime.now().date())
    data = {
        'total_orders_amount':
            orders.aggregate(Sum('amount'))['amount__sum'],
        'total_orders_served_amount':
            orders.filter(served=True).aggregate(Sum('amount'))['amount__sum']
    }
    if not data['total_orders_amount']:
        data['total_orders_amount'] = 0
    if not data['total_orders_served_amount']:
        data['total_orders_served_amount'] = 0
    data['total_amount_still_out'] = (
            data['total_orders_amount'] - data['total_orders_served_amount'])
    return JsonResponse(data)


def api_mark_order_served(request, id):
    """
    View for marking and unmarking the order as served.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    order = Order.objects.get(id=id)
    order.served = not order.served
    order.save()
    return HttpResponse('Marked as served')


def api_delete_order(request, id):
    """
    View for deleting an order.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    Order.objects.get(id=id).delete()
    return HttpResponse('Deleted.')
