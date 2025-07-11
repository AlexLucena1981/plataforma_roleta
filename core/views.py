# Imports necessários para o arquivo funcionar
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import mercadopago
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import HasActiveSubscription
from .models import Profile

from django.http import HttpResponse
from django.contrib.auth.models import User

# View para verificar o status do usuário logado
class UserStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        profile = request.user.profile
        content = {
            'username': request.user.username,
            'email': request.user.email,
            'status_assinatura': profile.subscription_status,
            'expira_em': profile.subscription_expires_at.strftime('%d/%m/%Y %H:%M') if profile.subscription_expires_at else 'N/A',
        }
        return Response(content)

# View de exemplo para uma ferramenta protegida
class FerramentaRoletaView(APIView):
    permission_classes = [HasActiveSubscription]

    def get(self, request, format=None):
        content = {
            'sucesso': True,
            'mensagem': f'Bem-vindo à ferramenta secreta, {request.user.username}!',
            'dados_da_ferramenta': {
                'numero_sorte': 17,
                'cor': 'Preto'
            }
        }
        return Response(content)

# View para criar um pagamento PIX, com debug
# core/views.py

# core/views.py

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = settings.MERCADOPAGO_ACCESS_TOKEN
        sdk = mercadopago.SDK(token)
        
        payment_data = {
            "transaction_amount": 1.00, # Use um valor baixo para testes
            "description": "Renovação Mensal - Plataforma de Análise",
            "payment_method_id": "pix",
            # AQUI ESTÁ A MUDANÇA IMPORTANTE:
            "external_reference": str(request.user.id),
            "payer": {
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            },
            "notification_url": "https://7aea26560d64.ngrok-free.app/api/webhook/mercadopago/",
        }

        try:
            payment_response = sdk.payment().create(payment_data)

            if "response" in payment_response and "error" in payment_response["response"]:
                return Response(payment_response["response"], status=400)
            
            payment = payment_response.get("response")
            if not payment:
                 return Response({"error": "Resposta inesperada do gateway de pagamento."}, status=500)
            
            return Response({
                "payment_id": payment["id"],
                "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
                "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"],
            })

        except Exception as e:
            return Response({"error": "Um erro inesperado ocorreu na aplicação."}, status=500)

# View para receber a confirmação de pagamento do Mercado Pago (webhook)


class MercadoPagoWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        print("--- WEBHOOK RECEBIDO DO MERCADO PAGO ---")
        print("DADOS:", request.data) 
        
        payment_id = None
        
        # Lógica para ler os dois formatos de webhook
        if request.data.get("action") == "payment.created" or request.data.get("action") == "payment.updated":
            payment_id = request.data.get("data", {}).get("id")
        elif request.data.get("topic") == "payment":
            payment_id = request.data.get("resource")

        if payment_id is None:
            print("!!! ERRO: 'payment_id' não encontrado nos dados do webhook.")
            return Response(status=status.HTTP_200_OK) # Retorna 200 para o MP não reenviar

        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        try:
            payment_info = sdk.payment().get(payment_id)["response"]

            if payment_info.get("status") == "approved":
                # AQUI USAMOS A EXTERNAL_REFERENCE PARA ACHAR O USUÁRIO
                user_id = payment_info.get("external_reference")
                if not user_id:
                    print("!!! ERRO: external_reference não encontrada no pagamento.")
                    return Response(status=status.HTTP_200_OK)

                user = User.objects.get(id=int(user_id))
                
                profile = user.profile
                if profile.subscription_expires_at and profile.subscription_expires_at > timezone.now():
                    profile.subscription_expires_at += datetime.timedelta(days=30)
                else:
                    profile.subscription_expires_at = timezone.now() + datetime.timedelta(days=30)
                
                profile.subscription_status = 'ATIVA'
                profile.save()
                print(f"--- ASSINATURA DO USUÁRIO '{user.username}' ATUALIZADA COM SUCESSO ---")
            
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"!!! ERRO AO PROCESSAR WEBHOOK: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def criar_superusuario_temporario(request):
    # Verifique se o usuário já não existe
    if User.objects.filter(username='admin').exists():
        return HttpResponse("O superusuário 'admin' já existe.")
    
    # Crie o superusuário com os dados desejados
    # IMPORTANTE: Use uma senha forte e troque-a depois!
    User.objects.create_superuser('alexandre.lucena', 'alexandre.lucena@gmail.com', 'Al32246391@')
    
    return HttpResponse("Superusuário 'admin' criado com sucesso! Agora você pode deletar esta URL e a view.")
