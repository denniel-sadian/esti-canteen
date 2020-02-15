"""
Views for the `canteen`
"""

from django.dispatch import receiver
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.utils.timezone import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core.signals import request_started
from django.core.signals import request_finished
from django.db.models import Sum
from django.db.models import Q
from django.db import close_old_connections

from .models import Dish
from .models import Order
from .models import Feedback
from .forms import UpdateOrderForm
from .forms import OrderForm
from .forms import FeedbackForm


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


@receiver(request_started)
def started_request(**kwargs):
    close_old_connections()


@receiver(request_finished)
def finished_request(**kwargs):
    close_old_connections()


class HomeView(ListView):
    """
    View for listing the dishes at home page.
    """
    context_object_name = 'dishes'

    def dispatch(self, request, *args, **kwargs):
        
        close_old_connections()
        
        # get the orders
        orders_today = get_orders(request)
        
        for o in request.session.get('orders', []):
            # remove the pk of the order if it does not exist
            if not Order.objects.filter(id=o).exists():
                self.request.session.get('orders').remove(o)
                self.request.session['orders'] = (
                    self.request.session.get('orders'))
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        close_old_connections()
        context = super().get_context_data(**kwargs)
        
        # get the sum of all orders today
        context['orders_count'] = Order.objects.filter(
            date__date=datetime.now().date()
            ).aggregate(Sum('count'))['count__sum']
        
        return context

    def get_queryset(self):
        close_old_connections()

        # order it by name
        return Dish.objects.filter(
            Q(date=datetime.now()) | Q(everyday=True)
        ).order_by('name')


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
        close_old_connections()
        context = super().get_context_data(**kwargs)
        
        # get the sum of all orders of this dish
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
        close_old_connections()

        # get the dish based from the pk
        self.dish = Dish.objects.get(id=kwargs['dish'])
        
        # redirect if ordering is not allowed
        if self.dish.sold_out:
            return HttpResponseRedirect(reverse_lazy('canteen:unable-to-order'))
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # assign the dish
        form.instance.dish = self.dish
        
        # upper the name
        form.instance.name = form.instance.name.upper()
        
        # save it now
        form.save()

        # create the orders holder in the session
        if type(self.request.session.get('orders')) != list:
            self.request.session['orders'] = []
        
        # get the orders from the session and add the new pk
        orders = self.request.session.get('orders')
        orders.append(form.instance.id)
        
        # assign the order again
        self.request.session['orders'] = orders

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        close_old_connections()
        context = super().get_context_data(**kwargs)
        
        # add the chosen dish in the context
        context['dish'] = self.dish
        
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
    form_class = FeedbackForm
    success_url = reverse_lazy('canteen:home')
    template_name = 'canteen/feedback_form.html'

    def form_valid(self, form):
        # upper the name
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
        close_old_connections()
        context = super().get_context_data(**kwargs)
        
        # add the everyday dishes
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
    success_url = reverse_lazy('canteen:manage-dishes')
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
    success_url = reverse_lazy('canteen:manage-dishes')
    model = Dish
    fields = ['name', 'price', 'description', 'sold_out', 'photo',
              'everyday', 'date']
    template_name = 'canteen/edit_dish.html'

    def form_valid(self, form):
        # Uppercase the name.
        form.instance.name = form.instance.name.upper()
        # Set the date.
        form.instance.date = datetime.now().date()
        return super().form_valid(form)


class UpdateOrderView(LoginRequiredMixin, UpdateView):
    """
    View for updating an order.
    """
    login_url = '/login/'
    success_url = reverse_lazy('canteen:orders')
    form_class = UpdateOrderForm
    model = Order
    template_name = 'canteen/edit_order.html'

    def form_valid(self, form):
        # Uppercase the name.
        form.instance.name = form.instance.name.upper()
        # Set the date.
        form.instance.date = datetime.now().date()
        return super().form_valid(form)


def not_found_view(request):
    return render(request, 'canteen/404.html')


def server_error_view(request):
    return render(request, 'canteen/500.html')


def bad_request_view(request):
    return render(request, 'canteen/403.html')


def permission_denied_view(request):
    return render(request, 'canteen/400.html')


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
