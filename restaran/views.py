from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, OrderSerializer
from .models import Order

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.conf import settings
from .models import TelegramUser

@method_decorator(csrf_exempt, name='dispatch')
class SaveChatIDView(View):
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Token {settings.BOT_API_TOKEN}":
            return JsonResponse({"error": "Unauthorized"}, status=401)

        data = json.loads(request.body)
        chat_id = data.get("chat_id")
        username = data.get("username")

        if not chat_id:
            return JsonResponse({"error": "chat_id required"}, status=400)

        TelegramUser.objects.get_or_create(chat_id=chat_id, defaults={"username": username})
        return JsonResponse({"status": "success"})
