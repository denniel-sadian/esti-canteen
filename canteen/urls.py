from django.urls import path, include
from django.contrib.auth.views import LoginView

from . import views
from . import api_urls

app_name = 'canteen'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.DishView.as_view(), name='not-api-dish-detail'),
    path('order/<int:dish>/', views.OrderView.as_view(), name='order'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('orders/', views.RealTimeOrdersView.as_view(), name='orders'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('json-orders/', views.json_orders, name='json-orders'),
    path('json-audit/', views.json_audit, name='json-audit'),
    path('json-feedbacks/', views.json_feedbacks, name='json-feedbacks'),
    path('api-mark-as-ready/<int:id>/',views.api_mark_order_ready,
         name='api-ready'),
    path('api-mark-as-served/<int:id>/',views.api_mark_order_served,
         name='api-served'),
    path('api-delete-order/<int:id>/', views.api_delete_order,
         name='api-delete-order'),
    path('api-delete-dish/<int:id>/', views.api_delete_dish,
         name='api-delete-dish'),
    
    path('manage/', views.ManageView.as_view(), name='manage'),
    path('manage/create/', views.CreateDishView.as_view(), name='create'),
    path('manage/edit-order/<int:pk>/', views.UpdateOrderView.as_view(), name='edit-order'),
    path('manage/edit/<int:pk>/', views.UpdateDishView.as_view(), name='edit'),
    path('login/', LoginView.as_view(
        template_name='canteen/login.html',
    )),

    path('api/', include(api_urls.urlpatterns))
]