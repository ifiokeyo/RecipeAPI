from rest_framework import serializers
from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model"""

    id = serializers.SerializerMethodField('get_id')
    total_price = serializers.DecimalField(
        max_digits=8, decimal_places=2,
        source='get_total_price', read_only=True
    )

    class Meta:
        model = Order
        fields = ('id', 'total_price', 'pizza_flavour', 'customer',
                  'size', 'quantity', 'status', 'created_at')
        read_only_Fields = ('id', 'status', 'customer', 'created_at')

    def get_id(self, obj):
        return obj.uuid
