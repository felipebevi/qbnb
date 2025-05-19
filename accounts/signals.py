from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Sinal para criar automaticamente um perfil quando um usuário é criado.
    """
    if created:
        # Usar get_or_create para evitar duplicidade
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Sinal para salvar o perfil quando o usuário é salvo.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Usar get_or_create para evitar duplicidade
        UserProfile.objects.get_or_create(user=instance)

@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    """
    Sinal para configurar o perfil quando um usuário se cadastra via social login.
    """
    # Garantir que o usuário tenha um perfil
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Por padrão, usuários de login social são clientes
    profile.is_client = True
    profile.save()

@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    """
    Sinal para atualizar o perfil quando uma conta social é adicionada a um usuário existente.
    """
    user = sociallogin.user
    # Usar get_or_create para evitar duplicidade
    UserProfile.objects.get_or_create(user=user)
