from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.first_name + " " + self.last_name
