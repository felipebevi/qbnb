from django.db import models
from django.contrib.auth.models import User
from properties.models import PropertyPeriod

class Reservation(models.Model):
    """
    Modelo para reservas de períodos de imóveis.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='Cliente')
    period = models.OneToOneField(PropertyPeriod, on_delete=models.CASCADE, related_name='reservation', verbose_name='Período')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    confirmed = models.BooleanField(default=False, verbose_name='Confirmado')
    confirmation_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de confirmação')
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reserva de {self.user.email} para {self.period.property.title}"
    
    def save(self, *args, **kwargs):
        # Marcar o período como reservado quando a reserva for criada
        if not self.pk:  # Nova reserva
            self.period.is_reserved = True
            self.period.save()
        super().save(*args, **kwargs)
