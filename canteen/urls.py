from django.urls import path

from . import views

app_name = 'canteen'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.DishView.as_view(), name='dish-detail'),
    path('order/<int:dish>/', views.OrderView.as_view(), name='order'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('orders/', views.RealTimeOrdersView.as_view(), name='orders'),
    path('json-orders/', views.json_orders, name='json-orders'),
    path('json-audit/', views.json_audit, name='json-audit'),
    path('api-mark-as-served/<int:id>/',views.api_mark_order_served,
         name='api-served'),
    path('api-delete-order/<int:id>/', views.api_delete_order,
         name='api-delete-order'),
]