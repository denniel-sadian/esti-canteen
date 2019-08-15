from django.contrib import admin

from .models import Dish
from .models import Order
from .models import Feedback


@admin.site.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'date', 'sold_out')


@admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish', 'count', 'amount', 'id_no',
                    'contact_no', 'date')


@admin.site.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_no', 'date')
