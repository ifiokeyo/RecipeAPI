from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Pizza
from pizza.serializers import PizzaSerializer


PIZZAS_URL = reverse('pizza:pizza-list')


class PublicPizzasApiTests(TestCase):
    """Test the publicly available Pizza API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required for retrieving pizzas"""

        res = self.client.get(PIZZAS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePizzasApiTests(TestCase):
    """Test the authorized user pizza API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='johnny@andela.com',
            password='password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_pizzas(self):
        """Test retrieving pizzas"""

        Pizza.objects.create(flavour='Vegan')
        Pizza.objects.create(flavour='Dessert')

        res = self.client.get(PIZZAS_URL)

        pizzas = Pizza.objects.all().order_by('-flavour')
        serializer = PizzaSerializer(pizzas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_pizza_successful(self):
        """Test creating a new pizza"""

        payload = {'flavour': 'Simple'}
        self.client.post(PIZZAS_URL, payload)

        exists = Pizza.objects.filter(
            flavour=payload['flavour']
        ).exists()
        self.assertTrue(exists)

    def test_create_pizza_invalid(self):
        """Test creating a new pizza with invalid payload"""
        payload = {'flavour': ''}
        res = self.client.post(PIZZAS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
