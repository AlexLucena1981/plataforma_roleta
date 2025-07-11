from django.contrib import admin
from .models import Profile, Payment

# Permite que você veja e edite os Perfis no admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_status', 'subscription_expires_at')

# Permite que você veja os Pagamentos no admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'amount', 'created_at')