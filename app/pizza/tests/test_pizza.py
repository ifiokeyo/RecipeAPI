import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Pizza
from pizza.serializers import PizzaSerializer


PIZZAS_URL = reverse('pizza:pizza-list')


def detail_url(pizza_uuid):
    """Return pizza detail URL"""
    return reverse('pizza:pizza-detail', args=[pizza_uuid])


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

        Pizza.objects.create(flavour='Vegan',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})
        Pizza.objects.create(flavour='Dessert',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})

        res = self.client.get(PIZZAS_URL)

        pizzas = Pizza.objects.all().order_by('-flavour')
        serializer = PizzaSerializer(pizzas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_pizza_successful(self):
        """Test creating a new pizza"""

        payload = {
            'flavour': 'Simple',
            'prices': json.dumps({"S": 10.00, "M": 15.00, "L": 20.00})
        }
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

    def test_partial_update_pizza(self):
        """Test updating a pizza with patch"""

        pizza = Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        payload = {'flavour': 'Dessert Vegan'}
        url = detail_url(pizza.uuid)
        self.client.patch(url, payload)

        pizza.refresh_from_db()
        self.assertEqual(pizza.flavour, payload['flavour'])

    def test_view_pizza_detail(self):
        """Test viewing a pizza detail"""

        pizza = Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        url = detail_url(pizza.uuid)
        res = self.client.get(url)

        serializer = PizzaSerializer(pizza)
        self.assertEqual(res.data, serializer.data)

    def test_delete_order(self):
        """Test deleting a pizza"""

        pizza1 = Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )
        Pizza.objects.create(flavour='Vegan',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})

        url = detail_url(pizza1.uuid)
        res = self.client.delete(url)

        pizza_state = Pizza.objects.all()

        pizza_serializer = PizzaSerializer(pizza_state, many=True)
        pizza1_serializer = PizzaSerializer(pizza1)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(pizza_state), 1)
        self.assertNotIn(pizza1_serializer.data, pizza_serializer.data)
