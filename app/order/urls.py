from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet, AdminOrderViewSet

router = DefaultRouter(trailing_slash=False)

router.register('orders', OrderViewSet)
router.register('admin', AdminOrderViewSet, basename='adminOrders')

app_name = 'order'


urlpatterns = [
    path('', include(router.urls))
]
