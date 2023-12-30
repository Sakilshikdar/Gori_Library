
from django import forms
from .models import Transaction
from .constants import DEPOSIT
from book.models import Post as Book


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')  # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        # ei field disable thakbe
        self.fields['transaction_type'].disabled = True
        # user er theke hide kora thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):  # amount field ke filter korbo
        min_deposit_amount = 100
        # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        return amount


class BorrowBookForm(TransactionForm):

    def clean_amount(self):
        book_price = 0
        book_id = self.cleaned_data.get('amount')
        book_no = book_id
        if book_id:
            try:
                book = Book.objects.get(id=book_id)
                self.cleaned_data['book_price'] = book.Price
                book_price = book.Price
            except Book.DoesNotExist:
                pass
        account = self.account
        balance = int(account.balance)  # 1000
        amount = int(book_price)  # 5000

        if amount > balance:  # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
        return amount
