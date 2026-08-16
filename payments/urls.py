from django.urls import path
from .views import FundWalletView, PaystackWebhookView

urlpatterns = [
    path('fund/', FundWalletView.as_view(), name='fund-wallet'),
    path('webhook/', PaystackWebhookView.as_view(), name='paystack-webhook'),
]