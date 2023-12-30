from django.shortcuts import render
from django.urls import reverse_lazy
from .import forms
from .import models
from .models import Transaction
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from .forms import DepositForm
from .models import Transaction
# from .utils import send_transaction_email
from .constants import DEPOSIT, BOWWOR_BOOK
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .forms import BorrowBookForm
from django.shortcuts import get_object_or_404
from book.models import Post
from django.db.models import Sum
from datetime import datetime


def send_transaction_email(user, to_user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    sent_email = EmailMultiAlternatives(
        subject, '', to=[to_user]
    )
    sent_email.attach_alternative(message, 'text/html')
    sent_email.send()


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    balance = 0
    success_url = reverse_lazy('deposit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # template e context data pass kora
        context.update({
            'title': self.title,
            'balance': self.balance,

        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        send_transaction_email(
            self.request.user,
            self.request.user.email,
            amount,
            'Deposit Money Notification',
            'deposite_email.html'
        )

        return super().form_valid(form)


class BowworBookView(TransactionCreateMixin):
    template_name = 'bowwor_form.html'
    form_class = BorrowBookForm
    title = 'Book Borrow By ID'
    success_url = reverse_lazy('profile')
    balance = 0

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'book_id': self.kwargs.get('book_id'),
            'book_name': self.kwargs.get('name'),
        })
        return context

    def get_initial(self):
        initial = {'transaction_type': BOWWOR_BOOK}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully bowwor book amount {"{:,.2f}".format(float(amount))}$'
        )
        # print(self.request.user.account.balance)
        # print(self.request.user.account)
        # print(self.request.user)
        # print(amount)

        send_transaction_email(
            self.request.user,
            self.request.user.email,
            amount,
            'Borrow Book Notification',
            'withdraw_email.html'
        )

        return super().form_valid(form)

    # unique queryset hote hobe


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transaction_report.html'
    model = Transaction
    balance = 0  # filter korar pore ba age amar total balance ke show korbe

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance

        return queryset.distinct()  # unique queryset hote hobe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        transactions = context['object_list']
        # print(transactions.values())
        # book_names = [
        #     transaction.book.name for transaction in transactions if transaction.book]
        # context['book_names'] = book_names

        return context
