from .models import Discount
from rest_framework import serializers


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'code', 'amount', 'percentage']
