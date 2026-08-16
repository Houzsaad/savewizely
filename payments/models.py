from django.db import models

from accounts.models import User
from accounts.models import LockedSavings
from accounts.models import SavingsGoal

class Transaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = 'deposit', 'Deposit'
        WITHDRAWAL = 'withdrawal', 'Withdrawal'
        LOCK = 'lock', 'Lock Savings'
        UNLOCK = 'unlock', 'Unlock Savings'
        GOAL_CONTRIBUTION = 'goal_contribution', 'Goal Contribution'
        PENALTY = 'penalty', 'Penalty Fee'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    reference = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length=255, blank=True)
    locked_savings = models.ForeignKey(LockedSavings, null=True, blank=True, on_delete=models.SET_NULL)
    goal = models.ForeignKey(SavingsGoal, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'created_at'])]
        
# Create your models here.
