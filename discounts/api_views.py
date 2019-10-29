from .models import Discount
from .serializers import DiscountSerializer
from rest_framework import viewsets


class DiscountApiViewSet(viewsets.ModelViewSet):
    """
    Endpoint to allow courses to be viewed on frontend
    """
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = DiscountSerializer
