import uuid
import requests
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer


class FundWalletView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        amount = request.data.get('amount')

        if not amount:
            return Response({'error': 'Amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Amount must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        reference = str(uuid.uuid4())
        amount_kobo = int(amount * 100)

        paystack_response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers={
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "email": request.user.email,
                "amount": amount_kobo,
                "reference": reference,
            },
        )

        paystack_data = paystack_response.json()

        if not paystack_data.get('status'):
            return Response(
                {'error': 'Failed to initialize payment.', 'details': paystack_data},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        transaction = Transaction.objects.create(
            user=request.user,
            reference=reference,
            type=Transaction.Type.DEPOSIT,
            amount=amount,
            status=Transaction.Status.PENDING,
            description='Wallet funding via Paystack',
        )

        return Response(
            {
                'authorization_url': paystack_data['data']['authorization_url'],
                'reference': transaction.reference,
            },
            status=status.HTTP_201_CREATED,
        )