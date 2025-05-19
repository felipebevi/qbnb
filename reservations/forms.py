from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    """
    Formulário para criação de reservas.
    """
    class Meta:
        model = Reservation
        fields = []  # Não precisamos de campos adicionais, apenas o período que será passado via view
        
    def __init__(self, *args, **kwargs):
        self.period = kwargs.pop('period', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        
        # Verificar se o período já está reservado
        if self.period and self.period.is_reserved:
            raise forms.ValidationError("Este período já está reservado.")
        
        # Verificar se o usuário está tentando reservar seu próprio imóvel
        if self.period and self.user and self.period.property.owner == self.user:
            raise forms.ValidationError("Você não pode reservar seu próprio imóvel.")
            
        return cleaned_data
