from django.urls import path
from .import views


# app_name = 'transactions'
urlpatterns = [
    path("deposit/", views.DepositMoneyView.as_view(), name="deposit"),
    path("borrow/<int:book_id>/<str:name>/",
         views.BowworBookView.as_view(), name="borrow"),
    path("report/", views.TransactionReportView.as_view(),
         name="transaction_report"),
]
