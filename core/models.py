from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Opções para o status da assinatura
SUBSCRIPTION_CHOICES = (
    ('ATIVA', 'Ativa'),
    ('INATIVA', 'Inativa'),
    ('TESTE', 'Teste'),
)

class Profile(models.Model):
    # Associa o Perfil a um Usuário do Django. Se o usuário for deletado, o perfil também será.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Status da assinatura, usando as opções que definimos acima.
    subscription_status = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='TESTE')
    
    # Data e hora que a assinatura expira.
    subscription_expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# Função para criar o perfil automaticamente quando um novo usuário for criado
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Define a expiração inicial para 7 dias a partir de agora
        expires_at = timezone.now() + datetime.timedelta(days=7)
        Profile.objects.create(user=instance, subscription_expires_at=expires_at)

# Conecta a função ao "sinal" de criação de usuário do Django
models.signals.post_save.connect(create_user_profile, sender=User)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id_gateway = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pendente')

    def __str__(self):
        return f'{self.user.username} - R$ {self.amount}'