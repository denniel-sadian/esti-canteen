from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('dishes', api_views.DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feedbacks/', api_views.FeedbackListView.as_view(), name='feedbacks')
]
