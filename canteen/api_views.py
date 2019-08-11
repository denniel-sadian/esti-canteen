from django.utils.timezone import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .serializers import DishSerializer
from .serializers import OrderSerializer
from .serializers import FeedbackSerializer
from .models import Dish
from .models import Order
from .models import Feedback


class DishViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def get_queryset(self):
        return Dish.objects.filter(
            date=datetime.now()).annotate(Count('order'))


class OrderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class FeedbackListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
