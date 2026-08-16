import uuid
import hmac
import hashlib
import requests

from django.conf import settings
from django.db import transaction as db_transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

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


@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        paystack_signature = request.headers.get("x-paystack-signature")

        if not paystack_signature:
            return Response(
                {"detail": "Missing Paystack signature."},
                status=status.HTTP_400_BAD_REQUEST
            )

        raw_body = request.body

        expected_signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
            raw_body,
            hashlib.sha512
        ).hexdigest()

        if not hmac.compare_digest(paystack_signature, expected_signature):
            return Response(
                {"detail": "Invalid signature."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        event = request.data.get("event")
        data = request.data.get("data", {})

        if event != "charge.success":
            return Response({"detail": "Event ignored."}, status=status.HTTP_200_OK)

        reference = data.get("reference")
        paystack_amount = data.get("amount")
        payment_status = data.get("status")

        if not reference or paystack_amount is None:
            return Response(
                {"detail": "Invalid webhook data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with db_transaction.atomic():
            try:
                payment = Transaction.objects.select_for_update().get(reference=reference)
            except Transaction.DoesNotExist:
                return Response(
                    {"detail": "Transaction not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if payment.status == Transaction.Status.SUCCESS:
                return Response(
                    {"detail": "Transaction already processed."},
                    status=status.HTTP_200_OK
                )

            if payment_status != "success":
                return Response(
                    {"detail": "Payment was not successful."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            expected_amount = int(payment.amount * 100)

            if int(paystack_amount) != expected_amount:
                return Response(
                    {"detail": "Payment amount mismatch."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            wallet = payment.user.wallet
            wallet.balance += payment.amount
            wallet.save(update_fields=["balance"])

            payment.status = Transaction.Status.SUCCESS
            payment.save(update_fields=["status"])

        return Response(
            {"detail": "Webhook processed successfully."},
            status=status.HTTP_200_OK
        )