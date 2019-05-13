from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
	PermissionsMixin


class UserManager(BaseUserManager):

	def create_user(self, email, password=None, **extra_fields):
		"""creates and saves a new user"""

		if email is None or not email:
			raise ValueError('email field is required')

		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):
		"""creates and saves a new superuser"""

		user = self.create_user(email=email, password=password)

		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""Custom user model that supports email and password instead of username"""

	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'

	objects = UserManager()

	def __str__(self):
		"""returns a user's email"""
		return self.email
