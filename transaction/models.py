from django.db import models
from author.models import UserBankAccount
# Create your models here.
from .constants import TRANSACTION_TYPE


class Transaction(models.Model):
    # ekjon user er multiple transactions hote pare
    account = models.ForeignKey(
        UserBankAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.IntegerField()
    balance_after_transaction = models.DecimalField(
        decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
