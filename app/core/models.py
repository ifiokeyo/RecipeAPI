import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Pizza(models.Model):
    """Pizza model to hold different flavours"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True,
                            editable=False)
    flavour = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.flavour


class Order(models.Model):
    """Order model to hold pizza orders from users"""

    LARGE = 'L'
    MEDIUM = 'M'
    SMALL = 'S'
    PENDING = 'P'
    IN_PROGRESS = 'I'
    DONE = 'DN'
    DELIVERED = 'DL'

    PIZZA_SIZE_CHOICES = [
        (LARGE, 'Large'),
        (MEDIUM, 'Medium'),
        (SMALL, 'small'),
    ]

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In-progress'),
        (DONE, 'Done'),
        (DELIVERED, 'Delivered')
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True,
                            editable=False)
    customer = models.ForeignKey(User, related_name='orders',
                                 on_delete=models.CASCADE)
    pizza_flavour = models.ForeignKey(Pizza, related_name='orders',
                                      on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=PIZZA_SIZE_CHOICES,
                            default=SMALL)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(2147483647)
        ],
        help_text='number of pizza-box'
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
