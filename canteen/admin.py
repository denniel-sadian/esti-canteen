from django.contrib import admin

from .models import Dish
from .models import Order
from .models import Feedback


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'date', 'sold_out')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish', 'count', 'amount', 'id_no',
                    'contact_no', 'date')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')


admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
