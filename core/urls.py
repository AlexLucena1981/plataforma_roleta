# core/urls.py
from django.urls import path
from .views import UserStatusView, FerramentaRoletaView, CreatePaymentView

urlpatterns = [
    path('status/', UserStatusView.as_view(), name='user-status'),
    path('ferramenta1/', FerramentaRoletaView.as_view(), name='ferramenta-roleta'),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
]