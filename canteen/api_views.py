from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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


class OrderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
