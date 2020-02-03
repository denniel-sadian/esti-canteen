"""
The routing part of all the views.
"""


from django.urls import path, include
from django.contrib.auth.views import LoginView

from . import views
from . import api_urls

app_name = 'canteen'
urlpatterns = [
    # The home page
    path('', views.HomeView.as_view(), name='home'),
    
    # The detail of the dish
    path('<int:pk>/', views.DishView.as_view(), name='not-api-dish-detail'),
    
    # The order form of the dish
    path('order/<int:dish>/', views.OrderView.as_view(), name='order'),
    
    # The thanking page when done ordering
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    
    # The page that tells ordering is not allowed
    path('invalid-order/', views.UnableToOrderView.as_view(), name='unable-to-order'),
    
    # The about page
    path('about/', views.AboutView.as_view(), name='about'),
    
    # The privacy policy page
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    
    # The feedback form
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    
    # The JSON report dictionary
    path('json-report/', views.json_report, name='json-report'),
    
    # The JSON customer's orders dictionary
    path('json-customer-orders/', views.json_customer_orders, name='json-customer-orders'),
    
    # The API for marking the order as ready
    path('api-mark-as-ready/<int:id>/',views.api_mark_order_ready,
         name='api-ready'),
    
    # The API for marking the order as served
    path('api-mark-as-served/<int:id>/',views.api_mark_order_served,
         name='api-served'),
    
    # The API for deleting an order
    path('api-delete-order/<int:id>/', views.api_delete_order,
         name='api-delete-order'),
    
    # The API for deleting a dish
    path('api-delete-dish/<int:id>/', views.api_delete_dish,
         name='api-delete-dish'),
    
    # The API for deleting a feedback
    path('api-delete-feedback/<int:id>/', views.api_delete_feedback,
         name='api-delete-feedback'),
    
    # The managing page of the dishes
    path('manage/dish/', views.ManageView.as_view(), name='manage-dishes'),

    # The form for creating the dish
    path('manage/dish/create/', views.CreateDishView.as_view(), name='create'),

    # The page for the realtime orders and others
    path('manage/orders/', views.RealTimeOrdersView.as_view(), name='orders'),
    
    # The form for updating an order
    path('manage/edit-order/<int:pk>/', views.UpdateOrderView.as_view(), name='edit-order'),
    
    # The form for updating a dish
    path('manage/edit/<int:pk>/', views.UpdateDishView.as_view(), name='edit'),
    
    # The login page
    path('login/', LoginView.as_view(
        template_name='canteen/login.html',
    )),

    # The root of the "real" API that is useless
    path('api/', include(api_urls.urlpatterns))
]