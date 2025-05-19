from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário personalizado para criação de usuário com campos adicionais
    para o perfil (anunciante/cliente).
    """
    email = forms.EmailField(required=True, label='E-mail')
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    is_advertiser = forms.BooleanField(required=False, label='Quero anunciar imóveis')
    is_client = forms.BooleanField(required=False, initial=True, label='Quero alugar imóveis')
    phone = forms.CharField(max_length=20, required=False, label='Telefone')
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar os campos obrigatórios mais evidentes
        for field_name in self.fields:
            if self.fields[field_name].required:
                self.fields[field_name].widget.attrs['class'] = 'form-control required'
                self.fields[field_name].widget.attrs['placeholder'] = f'{self.fields[field_name].label} *'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control'
                self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Usar email como username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Atualizar o perfil do usuário
            user.profile.is_advertiser = self.cleaned_data.get('is_advertiser', False)
            user.profile.is_client = self.cleaned_data.get('is_client', True)
            user.profile.phone = self.cleaned_data.get('phone', '')
            user.profile.save()
        
        return user

class UserProfileForm(forms.ModelForm):
    """
    Formulário para edição do perfil do usuário.
    """
    class Meta:
        model = UserProfile
        fields = ('is_advertiser', 'is_client', 'phone', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
