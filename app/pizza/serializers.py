from rest_framework import serializers

from core.models import Pizza


class PizzaSerializer(serializers.ModelSerializer):
    """Serializer for the Pizza model"""

    id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = Pizza
        fields = ('id', 'flavour', 'prices', 'created_at')
        read_only_Fields = ('id', 'created_at')

    def get_id(self, obj):
        return obj.uuid
