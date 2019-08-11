from rest_framework.viewsets import ModelViewSet

from .serializers import DishSerializer
from .serializers import OrderSerializer
from .serializers import FeedbackSerializer
from .models import Dish
from .models import Order
from .models import Feedback


class DishViews(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = AccountSerializer
