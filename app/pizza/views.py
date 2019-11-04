from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Pizza

from pizza import serializers


class PizzaViewSet(viewsets.ModelViewSet):
    """Manage pizza in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Pizza.objects.all()
    serializer_class = serializers.PizzaSerializer

    def perform_create(self, serializer):
        """Create a new pizza"""
        serializer.save()
