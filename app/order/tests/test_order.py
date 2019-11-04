from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Pizza, Order
from order.serializers import OrderSerializer


ORDER_URL = reverse('order:order-list')


def detail_url(order_uuid):
    """Return order detail URL"""
    return reverse('order:order-detail', args=[order_uuid])


def create_orders(pizza_list, user, **kwargs):
    return [Order.objects.create(customer=user, pizza_flavour=pizza, **kwargs)
            for pizza in pizza_list]


class PublicOrderApiTests(TestCase):
    """Test the publicly available Order API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required for retrieving pizza orders"""

        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):
    """Test the authorized user order API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='johnny@andela.com',
            password='password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_orders(self):
        """Test retrieving pizza orders"""

        Pizza.objects.create(flavour='Vegan',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})
        Pizza.objects.create(flavour='Dessert',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})

        pizzas = Pizza.objects.all().order_by('-flavour')
        orders = create_orders(pizzas, self.user)

        res = self.client.get(ORDER_URL)

        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_orders_limited_to_user(self):
        """Test that orders returned are for authenticated user"""

        user2 = get_user_model().objects.create_user(
            'other@andela.com',
            'testpass'
        )

        pizza1 = Pizza.objects.create(
            flavour='Vegan',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )
        pizza2 = Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        Order.objects.create(customer=user2, pizza_flavour=pizza1)
        order = Order.objects.create(customer=self.user, pizza_flavour=pizza2)

        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['pizza_flavour'], order.pizza_flavour.uuid)

    def test_create_order_successful(self):
        """Test creating a new Pizza Order"""

        pizza = Pizza.objects.create(
            flavour='Vegan',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        payload = {'pizza_flavour': pizza.flavour}
        self.client.post(ORDER_URL, payload)

        exists = Order.objects.filter(
            pizza_flavour=pizza.uuid
        ).exists()
        self.assertTrue(exists)

    def test_create_order_invalid(self):
        """Test creating a new pizza order with invalid payload"""
        payload = {'flavour': '', 'size': ''}
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_order_detail(self):
        """Test viewing an order detail"""

        Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        pizzas = Pizza.objects.all().order_by('-flavour')
        orders = create_orders(pizzas, self.user)

        url = detail_url(orders[0].uuid)
        res = self.client.get(url)

        serializer = OrderSerializer(orders[0])
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_order(self):
        """Test updating an order with patch"""

        Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        pizzas = Pizza.objects.all().order_by('-flavour')
        orders = create_orders(pizzas, self.user)

        payload = {'size': 'M'}
        url = detail_url(orders[0].uuid)
        self.client.patch(url, payload)

        orders[0].refresh_from_db()
        self.assertEqual(orders[0].size, payload['size'])

    def test_update_order_status_delivered_fail(self):
        """Test updating an order with status as delivered fails"""
        Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        pizzas = Pizza.objects.all().order_by('-flavour')
        orders = create_orders(pizzas, self.user, status='DL')

        payload = {'status': 'P'}
        url = detail_url(orders[0].uuid)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order(self):
        """Test deleting an order"""

        Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )
        Pizza.objects.create(flavour='Vegan',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})

        pizzas = Pizza.objects.all().order_by('-flavour')
        orders = create_orders(pizzas, self.user)

        url = detail_url(orders[0].uuid)
        res = self.client.delete(url)

        orders_state = Order.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(orders_state), 1)
        self.assertNotEqual(orders_state[0].uuid, orders[0].uuid)

    def test_delete_for_order_not_found(self):
        """Test deleting an order belonging to another user"""

        user2 = get_user_model().objects.create_user(
            email='test@andela.com',
            password='password'
        )

        Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )
        Pizza.objects.create(flavour='Vegan',
                             prices={"S": 10.00, "M": 15.00, "L": 20.00})

        pizzas = Pizza.objects.all().order_by('-flavour')
        orders = create_orders(pizzas, user2)

        url = detail_url(orders[0].uuid)
        res = self.client.delete(url)

        orders_state = Order.objects.all()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(orders_state), 2)

    def test_filter_order_by_status(self):
        """Test filtering order by status"""

        Pizza.objects.create(
            flavour='Dessert',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )
        Pizza.objects.create(
            flavour='Vegan',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        Pizza.objects.create(
            flavour='Ankara',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )
        Pizza.objects.create(
            flavour='Bali',
            prices={"S": 10.00, "M": 15.00, "L": 20.00}
        )

        pizzas = Pizza.objects.all().order_by('-flavour')

        order1 = create_orders(
            pizzas[:2], self.user, status='I'
        )

        order2 = create_orders(
            pizzas[:2], self.user, status='P'
        )

        order_serializer1 = OrderSerializer(order1, many=True)
        order_serializer2 = OrderSerializer(order2, many=True)

        res = self.client.get(ORDER_URL, {'status': 'I,P'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(order_serializer1.data[0], res.data)
        self.assertIn(order_serializer1.data[1], res.data)
        self.assertIn(order_serializer2.data[0], res.data)
        self.assertIn(order_serializer2.data[1], res.data)
