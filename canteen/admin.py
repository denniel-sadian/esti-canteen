from django.contrib import admin

from .models import Dish
from .models import Order


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'date', 'sold_out')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish', 'count', 'amount', 'id_no',
                    'contact_no', 'date')


admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
