from rest_framework.permissions import BasePermission
from django.utils import timezone

class HasActiveSubscription(BasePermission):
    """
    Permite o acesso apenas a usuários autenticados com uma assinatura ativa.
    """
    message = 'Sua assinatura está inativa ou expirada.'

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica se o perfil do usuário tem uma data de expiração
        # e se essa data é no futuro.
        profile = request.user.profile
        if profile.subscription_expires_at and profile.subscription_expires_at > timezone.now():
            return True
        
        return False