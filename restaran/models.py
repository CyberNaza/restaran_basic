from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import requests


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
        # Build items text
        items_text = ""
        if isinstance(self.items, dict):
            for key, value in self.items.items():
                if isinstance(value, dict):
                    name = value.get("name", "Unknown")
                    qty = value.get("quantity", 1)
                    price = value.get("price", "")
                    items_text += f"- {name} x{qty} ({price})\n"
                    if "total_price" in value:
                        total_price = value["total_price"]
                else:
                    items_text += f"- {str(value)}\n"
            if "total_price" in self.items:
                items_text += f"\n💰 Total: {self.items['total_price']}\n"
        elif isinstance(self.items, list):
            for item in self.items:
                if isinstance(item, dict):
                    name = item.get("name", "Unknown")
                    qty = item.get("quantity", 1)
                    price = item.get("price", "")
                    items_text += f"- {name} x{qty} ({price})\n"
                else:
                    items_text += f"- {str(item)}\n"
        else:
            items_text = str(self.items)

        # Format the message
        text = (
            f"📦 New Order!\n"
            f"👤 User: {self.user.username} ({self.user.phone})\n"
            f"🛒 Items:\n{items_text}"
            f"📍 Address: {self.address or 'N/A'}\n"
            f"💳 Payment: {self.payment_method}\n"
            f"⏰ Time: {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

        for tg_user in TelegramUser.objects.all():
            try:
                requests.get(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    params={
                        "chat_id": tg_user.chat_id,
                        "text": text,
                        "parse_mode": "HTML"  # Ensures proper formatting
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
        # Format the message
        text = (
            f"📨 New Contact Message!\n"
            f"👤 Name: {self.name}\n"
            f"📧 Email: {self.email or 'N/A'}\n"
            f"📞 Phone: {self.phone or 'N/A'}\n"
            f"💬 Message: {self.message or 'N/A'}\n"
            f"⏰ Time: {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

        for tg_user in TelegramUser.objects.all():
            try:
                requests.get(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    params={
                        "chat_id": tg_user.chat_id,
                        "text": text,
                        "parse_mode": "HTML"  # Ensures proper formatting
                    }
                )
            except Exception as e:
                print(f"Telegram send error: {e}")