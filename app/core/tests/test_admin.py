from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

	def setUp(self):
		self.client = Client()
		self.admin_user = get_user_model().objects.create_superuser(
			email='admin@andela.com', password='Test123'
		)
		self.client.force_login(self.admin_user)
		self.user = get_user_model().objects.create_user(
			email='test@andela.com',
			password='test123',
			name='JohnBosco Ohia'
		)

	def test_user_listed(self):
		"""test users are listed on user page"""

		url = reverse('admin:core_user_changelist')
		res = self.client.get(url)

		self.assertContains(res, self.user.email)
		self.assertContains(res, self.user.name)

	def test_user_page_change(self):
		"""Test that the user edit page works"""
		url = reverse('admin:core_user_change', args=[self.user.id])
		res = self.client.get(url)

		self.assertEqual(res.status_code, 200)

	def test_create_user_page(self):
		"""test that the create user page works"""

		url = reverse('admin:core_user_add')
		res = self.client.get(url)

		self.assertEqual(res.status_code, 200)
