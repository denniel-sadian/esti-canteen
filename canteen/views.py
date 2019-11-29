"""
Views for the `canteen`
"""

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import HttpResponseRedirect

from .models import Dish
from .models import Order
from .models import Feedback
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm


def get_orders(request):
    """
    Utility function for getting orders.
    """
    try:
        return Order.objects.filter(
            date__date=request.GET['date']).order_by('-date')
    except MultiValueDictKeyError:
        return Order.objects.filter(
            date__date=datetime.now().date()).order_by('-date')


class HomeView(ListView):
    """
    View for listing the dishes at home page.
    """
    context_object_name = 'dishes'

    def dispatch(self, request, *args, **kwargs):
        orders_today = get_orders(request)
        for o in request.session.get('orders', []):
            try:
                order = orders_today.get(id=o)
            except ObjectDoesNotExist:
                self.request.session.get('orders').remove(o)
                self.request.session['orders'] = (
                    self.request.session.get('orders'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_count'] = Order.objects.filter(
            date__date=datetime.now().date()
            ).aggregate(Sum('count'))['count__sum']
        return context

    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())


class AboutView(TemplateView):
    """
    View for simply displaying the about page.
    """
    template_name = 'canteen/about.html'


class DishView(DetailView):
    """
    View for displaying the dish's detail.
    """
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            dish=self.object).aggregate(Sum('count'))['count__sum']
        return context


class OrderView(CreateView):
    """
    View for creating orders.
    """
    model = Order
    fields = ['name', 'id_no', 'contact_no', 'count']
    success_url = reverse_lazy('canteen:thanks')

    def get(self, request, *args, **kwargs):
        self.object = None
        dish = Dish.objects.get(id=kwargs['dish'])
        if dish.sold_out:
            return HttpResponseRedirect(reverse_lazy('canteen:unable-to-order'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.dish = Dish.objects.get(id=self.kwargs['dish'])
        form.save()
        orders = self.request.session.get('orders', [])
        orders.append(form.instance.id)
        self.request.session['orders'] = orders
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(id=self.kwargs['dish'])
        return context


class UnableToOrderView(TemplateView):
    """
    View for informing the customer that the order can't be allowed.
    """
    template_name = 'canteen/unable_to_order.html'


class FeedbackView(CreateView):
    """
    View for creating a feedback.
    """
    model = Feedback
    fields = ['name', 'contact_no', 'content']
    success_url = reverse_lazy('canteen:home')


class ThanksView(TemplateView):
    """
    View for simply thanking the customer.
    """
    template_name = 'canteen/thanks.html'


class RealTimeOrdersView(LoginRequiredMixin, TemplateView):
    """
    View for displaying the template for orders and report.
    """
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'canteen/real_time_orders.html'


class ManageView(LoginRequiredMixin, ListView):
    """
    Home view of the managing site.
    """
    login_url = '/login/'
    template_name = 'canteen/manage.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.filter(date=datetime.now())


class CreateDishView(LoginRequiredMixin, CreateView):
    """
    View for creating a dish.
    """
    login_url = '/login/'
    model = Dish
    fields = ['name', 'price', 'description', 'photo', 'everyday']
    success_url = reverse_lazy('canteen:manage')
    template_name = 'canteen/create_dish.html'


class UpdateDishView(LoginRequiredMixin, UpdateView):
    """
    View for updating a dish.
    """
    login_url = '/login/'
    success_url = reverse_lazy('canteen:manage')
    model = Dish
    fields = ['name', 'price', 'description', 'sold_out', 'photo', 'everyday']
    template_name = 'canteen/edit_dish.html'


class UpdateOrderView(LoginRequiredMixin, UpdateView):
    """
    View for updating an order.
    """
    login_url = '/login/'
    success_url = reverse_lazy('canteen:orders')
    form_class = OrderForm
    model = Order
    template_name = 'canteen/edit_order.html'


def json_customer_orders(request):
    """
    View for giving all the orders from the session.
    """
    orders_today = get_orders(request)
    orders_from_device = []
    for o in request.session.get('orders', []):
        try:
            order = orders_today.get(id=o)
            orders_from_device.append({
                'name': order.name,
                'dish': {
                    'name': order.dish.name,
                    'count': order.count,
                    'price': order.amount
                },
                'served': order.served,
                'ready': order.ready
            })
        except ObjectDoesNotExist:
            request.session.get('orders').remove(o)
            request.session['orders'] = request.session.get('orders')
    return JsonResponse(orders_from_device, safe=False)


def json_orders(request):
    """
    View for displaying all the current orders.
    """
    
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    orders = get_orders(request)
    
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
            'served': order.served,
            'ready': order.ready
        }
        for order in orders
    ]
    return JsonResponse(orders, safe=False)


def json_feedbacks(request):
    """
    View for giving the feedbacks.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    feedbacks = [
        {
            'id': f.id,
            'name': f.name,
            'content': f.content,
            'date': f.date
        }
        for f in Feedback.objects.all().order_by('-date')
    ]
    return JsonResponse(feedbacks, safe=False)


def json_audit(request):
    """
    View for displaying the audit.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")

    orders = get_orders(request)

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
    if not order.ready:
        return HttpResponseForbidden("This order is not yet ready!")
    order.served = not order.served
    order.save()
    return HttpResponse('Marked as served')


def api_mark_order_ready(request, id):
    """
    View for marking and unmarking the order as ready.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    order = Order.objects.get(id=id)
    order.ready = not order.ready
    order.save()
    return HttpResponse('Marked as ready')


def api_delete_order(request, id):
    """
    View for deleting an order.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    Order.objects.get(id=id).delete()
    return HttpResponse('Deleted.')


def api_delete_dish(request, id):
    """
    View for deleting a dish.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    Dish.objects.get(id=id).delete()
    return HttpResponse('Deleted.')
