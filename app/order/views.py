from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Pizza, Order

from order import serializers


class OrderViewSet(viewsets.ModelViewSet):
    """Manage pizza in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def _params_to_str(self, query_str):
        """Convert a list of string STATUS to a list of strings"""
        return [s_str for s_str in query_str.split(',')]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        status_params = self.request.query_params.get('status', None)

        queryset = self.queryset.filter(customer=self.request.user.id)

        if status_params is not None:
            status_ids = self._params_to_str(status_params)
            queryset = queryset.filter(status__in=status_ids)

        return queryset

    def create(self, request, *args, **kwargs):
        """prepares the request payload and creates a new pizza order"""

        flavour_payload = request.data.get('pizza_flavour', None)

        if flavour_payload is None:
            raise ValidationError({
                'message': 'This field cannot be empty!'
            })

        flavour = get_object_or_404(Pizza.objects.all(),
                                    flavour=flavour_payload)

        size = request.data.get('size', 'S')

        if size is None:
            raise ValidationError({
                'message': 'This field cannot be empty!'
            })

        quantity = request.data.get('quantity', 1)

        if not quantity:
            raise ValidationError({
                'message': 'This field cannot be empty!'
            })

        payload = {
            'pizza_flavour': flavour.uuid,
            'size': size,
            'quantity': quantity,
            'customer': self.request.user.id
        }

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        """Saves an order to the db"""
        serializer.save(customer=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.status == Order.DELIVERED:
            return Response({'message': 'Order has been delivered!'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class AdminOrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        """Return all objects for only an admin user """

        if not self.request.user.is_staff:
            raise ValidationError({
                'message': 'Permission Denied'
            })

        status_params = self.request.query_params.get('status', None)
        customer = self.request.query_params.get('customer', None)

        queryset = self.queryset

        if status_params is not None:
            status_ids = self._params_to_str(status_params)
            queryset = queryset.filter(status__in=status_ids)

        if customer is not None:
            queryset = queryset.filter(customer__email=customer)

        return queryset
