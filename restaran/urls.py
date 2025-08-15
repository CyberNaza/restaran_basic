from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from rest_framework.routers import DefaultRouter   


router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', MeView.as_view(), name='me'),

    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    

    path("api/save_chat_id/", SaveChatIDView.as_view(), name="save_chat_id"),


]
urlpatterns += router.urls