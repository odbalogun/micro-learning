from django.urls import path
from .views import PaymentHistoryView

app_name = 'payments'

urlpatterns = [
    path('payment-history', PaymentHistoryView.as_view(), name='payment-history'),
]