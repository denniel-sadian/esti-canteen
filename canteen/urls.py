from django.urls import path

from . import views

app_name = 'canteen'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.DishView.as_view(), name='dish-detail'),
    path('order/<int:dish>/', views.OrderView.as_view(), name='order'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('json-orders/', views.json_orders, name='json-orders')
]