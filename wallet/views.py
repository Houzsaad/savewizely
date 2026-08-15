from django.shortcuts import render
from .serializers import WalletSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status

class WalletView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer

    def get_object(self):
        return self.request.user.wallet

# Create your views here.
