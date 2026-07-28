from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    # profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)


# wallet/models.py
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


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
    reference = models.CharField(max_length=40, unique=True)  # generate via uuid
    type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LockedSavings(models.Model):
    class Frequency(models.TextChoices):
        DAILY = 'daily', 'Daily'
        WEEKLY = 'weekly', 'Weekly'
        MONTHLY = 'monthly', 'Monthly'
        YEARLY = 'yearly', 'Yearly'
        FIXED_DATE = 'fixed_date', 'Fixed Date'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        MATURED = 'matured', 'Matured'
        WITHDRAWN_EARLY = 'withdrawn_early', 'Withdrawn Early'
        COMPLETED = 'completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locked_savings')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    start_date = models.DateField(auto_now_add=True)
    unlock_date = models.DateField()
    early_withdrawal_penalty_pct = models.DecimalField(max_digits=4, decimal_places=2, default=5.00)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)


class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)  # e.g. "Buy Laptop"
    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    daily_target = models.DecimalField(max_digits=14, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    saved_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_streak = models.PositiveIntegerField(default=0)
    outstanding_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)  
    is_completed = models.BooleanField(default=False)


class GoalContribution(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField(auto_now_add=True)
  

class Transaction(models.Model):
    # ...existing fields...
    locked_savings = models.ForeignKey('savings.LockedSavings', null=True, blank=True, on_delete=models.SET_NULL)
    goal = models.ForeignKey('savings.SavingsGoal', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'created_at'])]


class LockedSavings(models.Model):
    # ...existing fields...
    class Meta:
        ordering = ['-start_date']

class SavingsGoal(models.Model):
    # ...existing fields...
    class Meta:
        ordering = ['-start_date']
# Create your models here.
