from django.urls import path

from . import views

app_name = 'canteen'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:id>/', views.HomeView.as_view(), name='dish-detail-view')
]