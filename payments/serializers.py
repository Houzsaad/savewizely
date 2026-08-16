from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'reference', 'type', 'amount', 'status', 'description', 'created_at']
        read_only_fields = ['reference', 'status', 'created_at']