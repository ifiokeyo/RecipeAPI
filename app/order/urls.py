from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet

router = DefaultRouter(trailing_slash=False)

router.register('orders', OrderViewSet)

app_name = 'order'


urlpatterns = [
    path('', include(router.urls))
]
