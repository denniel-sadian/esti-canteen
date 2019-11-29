from django.contrib import admin
from django.utils.timezone import datetime

from .models import Dish
from .models import Order
from .models import Feedback


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'date', 'sold_out', 'everyday')
    search_fields = ['name', 'description', 'price']


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'dish', 'count', 'amount', 'id_no',
                    'contact_no', 'date', 'served')


class FeedbackAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'contact_no', 'date')


admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
