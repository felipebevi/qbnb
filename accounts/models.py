from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Modelo para estender o usuário padrão do Django com campos adicionais
    para diferenciar entre anunciantes e clientes.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_advertiser = models.BooleanField(default=False, verbose_name='É anunciante')
    is_client = models.BooleanField(default=True, verbose_name='É cliente')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    bio = models.TextField(blank=True, null=True, verbose_name='Biografia')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return f'Perfil de {self.user.email}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Sinal para criar automaticamente um perfil quando um usuário é criado.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Sinal para salvar o perfil quando o usuário é salvo.
    """
    instance.profile.save()
