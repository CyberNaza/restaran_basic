from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    items = models.JSONField()  # store as {"pizza": 2, "burger": 3}
    address = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.item_price * self.item_quantity

    def __str__(self):
        return f"{self.user.username} - {self.item_name} x {self.item_quantity}"
