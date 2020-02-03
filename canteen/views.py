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
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import HttpResponseRedirect
from django.db import close_old_connections

from .models import Dish
from .models import Order
from .models import Feedback
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm


def get_orders(request):
    """
    Utility function for getting orders.
    """
    close_old_connections()
    try:
        # Give all orders maded on the given date.
        return Order.objects.filter(
            date__date=request.GET['date']).order_by('-date')
    except MultiValueDictKeyError:
        # Give all orders today.
        return Order.objects.filter(
            date__date=datetime.now().date()).order_by('-date')


class HomeView(ListView):
    """
    View for listing the dishes at home page.
    """
    context_object_name = 'dishes'

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding this method to remove the IDs of those orders
        that have been deleted already.
        """
        close_old_connections()
        orders_today = get_orders(request)
        for o in request.session.get('orders', []):
            if not Order.objects.filter(id=o).exists():
                self.request.session.get('orders').remove(o)
                self.request.session['orders'] = (
                    self.request.session.get('orders'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Overriding this method to add the count of the orders today.
        """
        close_old_connections()
        context = super().get_context_data(**kwargs)
        context['orders_count'] = Order.objects.filter(
            date__date=datetime.now().date()
            ).aggregate(Sum('count'))['count__sum']
        return context

    def get_queryset(self):
        """
        Overriding this method to reverse the order of the
        dishes by name.
        """
        close_old_connections()
        return Dish.objects.filter(
            Q(date=datetime.now()) | Q(everyday=True)
        ).order_by('-name')


class AboutView(TemplateView):
    """
    View for simply displaying the about page.
    """
    template_name = 'canteen/about.html'


class PrivacyPolicyView(TemplateView):
    """
    View for simply displaying the privacy policy.
    """
    template_name = 'canteen/privacypolicy.html'


class DishView(DetailView):
    """
    View for displaying the dish's detail.
    """
    model = Dish

    def get_context_data(self, **kwargs):
        """
        Overriding this method to reverse the order of the
        dishes by name.
        """
        close_old_connections()
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            dish=self.object).aggregate(Sum('count'))['count__sum']
        return context


class OrderView(CreateView):
    """
    View for creating orders.
    """
    form_class = OrderForm
    template_name = 'canteen/order_form.html'
    success_url = reverse_lazy('canteen:thanks')

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding this method to restrict the customer
        in ordering dishes that are already sold out.
        """
        close_old_connections()
        self.dish = Dish.objects.get(id=kwargs['dish'])
        if self.dish.sold_out:
            return HttpResponseRedirect(reverse_lazy('canteen:unable-to-order'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overriding this method to append the order's ID to the customer's
        session.
        """
        form.instance.dish = self.dish
        form.instance.name = form.instance.name.upper()
        form.save()
        if type(self.request.session.get('orders')) != list:
            self.request.session['orders'] = []
        orders = self.request.session.get('orders')
        orders.append(form.instance.id)
        self.request.session['orders'] = orders
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Overriding this method to add the dish in the context.
        """
        close_old_connections()
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

    def form_valid(self, form):
        """
        Overriding this method to uppercase the name.
        """
        form.instance.name = form.instance.name.upper()
        return super().form_valid(form)


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
        close_old_connections()
        try:
            # Give the dishes that were created on the given date
            # and are not for everyday.
            return Dish.objects.filter(
                date=self.request.GET['date'],
                everyday=False
            ).order_by('name')
        except MultiValueDictKeyError:
            # Give the dishes that were created today and are not
            # for everyday.
            return Dish.objects.filter(
                date=datetime.now(),
                everyday=False
            ).order_by('name')
    
    def get_context_data(self, **kwargs):
        """
        Adding the everyday dishes to the context.
        """
        close_old_connections()
        context = super().get_context_data(**kwargs)
        context['everyday_dishes'] = Dish.objects.filter(
            everyday=True).order_by('name')
        return context


class CreateDishView(LoginRequiredMixin, CreateView):
    """
    View for creating a dish.
    """
    login_url = '/login/'
    model = Dish
    fields = ['name', 'price', 'description', 'photo', 'everyday']
    success_url = reverse_lazy('canteen:manage')
    template_name = 'canteen/create_dish.html'

    def form_valid(self, form):
        # Uppercase the name.
        form.instance.name = form.instance.name.upper()
        # Set the date.
        form.instance.date = datetime.now().date()
        return super().form_valid(form)


class UpdateDishView(LoginRequiredMixin, UpdateView):
    """
    View for updating a dish.
    """
    login_url = '/login/'
    success_url = reverse_lazy('canteen:manage')
    model = Dish
    fields = ['name', 'price', 'description', 'sold_out', 'photo',
              'everyday', 'date']
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


def json_report(request):
    """
    View for giving the report.
    """

    close_old_connections()

    # Not allow unauthenticated users.
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    # Get orders.
    orders = get_orders(request)

    # Form the audit.
    audit = {
        'total_orders_amount': 0,
        'total_orders_served_amount': 0
    }
    for order in orders:
        amount = order.count * order.dish.price
        if order.served:
            audit['total_orders_served_amount'] += amount
        audit['total_orders_amount'] += amount
    audit['total_amount_still_out'] = (
            audit['total_orders_amount'] - audit['total_orders_served_amount'])
    
    # Form the orders.
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
            'amount': order.count * order.dish.price,
            'served': order.served,
            'ready': order.ready
        }
        for order in orders
    ]

    # Form the feedbacks.
    feedbacks = [
        {
            'id': f.id,
            'name': f.name,
            'content': f.content,
            'number': f.contact_no,
            'date': f.date
        }
        for f in Feedback.objects.all().order_by('-date')
    ]

    close_old_connections()

    return JsonResponse({
        'orders': orders,
        'feedbacks': feedbacks,
        'audit': audit
    })


def json_customer_orders(request):
    """
    View for giving all the orders from the session.
    """

    close_old_connections()

    # Get orders.
    orders_today = get_orders(request)
    orders_from_device = []
    
    for o in request.session.get('orders', []):
        try:
            # Get the orders.
            order = orders_today.get(id=o)
            orders_from_device.append({
                'name': order.name,
                'dish': {
                    'name': order.dish.name,
                    'count': order.count,
                    'price': order.count * order.dish.price
                },
                'served': order.served,
                'ready': order.ready
            })
        except ObjectDoesNotExist:
            # Remove the order's ID if it does not exist anymore.
            request.session.get('orders').remove(o)
            request.session['orders'] = request.session.get('orders')
    
    close_old_connections()
    
    return JsonResponse(orders_from_device, safe=False)


def api_mark_order_served(request, id):
    """
    View for marking and unmarking the order as served.
    """

    close_old_connections()
    
    # Not allow unauthenticated users.
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    # Get the order.
    order = Order.objects.get(id=id)
    
    # Not marking it as served if it isn't even ready yet.
    if not order.ready:
        return HttpResponseForbidden("This order is not yet ready!")
    
    # Mark it as served and save it.
    order.served = not order.served
    order.save()

    close_old_connections()

    return HttpResponse('Marked as served')


def api_mark_order_ready(request, id):
    """
    View for marking and unmarking the order as ready.
    """

    close_old_connections()
    
    # Not marking it as served if it isn't even ready yet.
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    # Get the order.
    order = Order.objects.get(id=id)
    
    # Mark the order as served and save it.
    order.ready = not order.ready
    order.save()

    close_old_connections()

    return HttpResponse('Marked as ready')


def api_delete_order(request, id):
    """
    View for deleting an order.
    """

    close_old_connections()

    # Not marking it as served if it isn't even ready yet.
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    # Delete the order.
    Order.objects.get(id=id).delete()

    close_old_connections()
    
    return HttpResponse('Deleted.')


def api_delete_dish(request, id):
    """
    View for deleting a dish.
    """

    close_old_connections()
    
    # Not marking it as served if it isn't even ready yet.
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    # Delete the dish.
    Dish.objects.get(id=id).delete()

    close_old_connections()
    
    return HttpResponse('Deleted.')


def api_delete_feedback(request, id):
    """
    View for deleting a feedback.
    """

    close_old_connections()
    
    # Not marking it as served if it isn't even ready yet.
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You're not authenticated.")
    
    # Delete the feedback.
    Feedback.objects.get(id=id).delete()

    close_old_connections()
    
    return HttpResponse('Deleted.')
