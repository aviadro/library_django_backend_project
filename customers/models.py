from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Customer(AbstractUser):
    city = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], blank=True, null=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.username