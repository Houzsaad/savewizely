from django.urls import path
from .views import FundWalletView

urlpatterns = [
    path('fund/', FundWalletView.as_view(), name='fund-wallet'),
]