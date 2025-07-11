# plataforma_roleta/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import MercadoPagoWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoints de Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Renovar token
    
    # Inclui as URLs do nosso app 'core'
    path('api/user/', include('core.urls')),
    path('api/webhook/mercadopago/', MercadoPagoWebhookView.as_view(), name='mp-webhook'),
]

    