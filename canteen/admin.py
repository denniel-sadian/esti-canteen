from django.contrib import admin
from django.utils.timezone import datetime

from .models import Dish
from .models import Order
from .models import Feedback


class DishAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'price', 'description', 'date', 'sold_out')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(date=datetime.now())


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'dish', 'count', 'amount', 'id_no',
                    'contact_no', 'date')


class FeedbackAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'contact_no', 'date')


admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
