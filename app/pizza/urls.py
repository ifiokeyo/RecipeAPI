from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pizza.views import PizzaViewSet

router = DefaultRouter(trailing_slash=False)

router.register('pizzas', PizzaViewSet)

app_name = 'pizza'


urlpatterns = [
    path('', include(router.urls))
]
