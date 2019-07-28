from django.contrib import admin

from .models import Dish
from .models import Order


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'description', 'sold_out')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_no', 'dish', 'count', 'amount', 'date')


admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
