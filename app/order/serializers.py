from rest_framework import serializers
from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model"""

    id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = Order
        fields = ('id', 'pizza_flavour', 'customer', 'size', 'quantity',
                  'status', 'created_at')
        read_only_Fields = ('id', 'status', 'customer', 'created_at')

    def get_id(self, obj):
        return obj.uuid
