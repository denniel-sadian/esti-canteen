from django.urls import path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register(r'dishes', api_views.DishViews)

urlpatterns = [
    path('', include(router.urls)),
]
