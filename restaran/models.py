from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import requests
import json


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    REQUIRED_FIELDS = ["phone"]


class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username or str(self.chat_id)


class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.JSONField()
    address = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_method} - {self.items}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_to_telegram()

    def send_to_telegram(self):
        # Prepare order data as a dictionary
        order_data = {
            "type": "order",
            "user": {
                "username": self.user.username,
                "phone": self.user.phone
            },
            "items": self.items,
            "address": self.address or "N/A",
            "payment_method": self.payment_method,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M')
        }
        
        # Convert to JSON string with proper encoding
        text = json.dumps(order_data, ensure_ascii=False, indent=2)

        for tg_user in TelegramUser.objects.all():
            try:
                requests.get(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    params={
                        "chat_id": tg_user.chat_id,
                        "text": text,
                        "parse_mode": "HTML"  # Using HTML to preserve JSON formatting
                    }
                )
            except Exception as e:
                print(f"Telegram send error: {e}")


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_to_telegram()

    def send_to_telegram(self):
        # Prepare contact data as a dictionary
        contact_data = {
            "type": "contact",
            "name": self.name,
            "email": self.email or "N/A",
            "phone": self.phone or "N/A",
            "message": self.message or "N/A",
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M')
        }
        
        # Convert to JSON string with proper encoding
        text = json.dumps(contact_data, ensure_ascii=False, indent=2)

        for tg_user in TelegramUser.objects.all():
            try:
                requests.get(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    params={
                        "chat_id": tg_user.chat_id,
                        "text": text,
                        "parse_mode": "HTML"  # Using HTML to preserve JSON formatting
                    }
                )
            except Exception as e:
                print(f"Telegram send error: {e}")