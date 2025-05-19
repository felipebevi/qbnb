from django import forms
from .models import Property, PropertyPhoto, PropertyPeriod
from django.forms import inlineformset_factory

class PropertyForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de imóveis.
    """
    class Meta:
        model = Property
        fields = ('title', 'description', 'address', 'city', 'state', 'zip_code', 'price')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.TextInput(attrs={'placeholder': 'Rua, número, complemento'}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

class PropertyPhotoForm(forms.ModelForm):
    """
    Formulário para upload de fotos de imóveis.
    """
    class Meta:
        model = PropertyPhoto
        fields = ('image', 'caption', 'is_main')
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Descrição da foto'}),
        }

class PropertyPeriodForm(forms.ModelForm):
    """
    Formulário para definição de períodos disponíveis para aluguel.
    """
    class Meta:
        model = PropertyPeriod
        fields = ('start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Formsets para gerenciar múltiplas fotos e períodos
PropertyPhotoFormSet = inlineformset_factory(
    Property, PropertyPhoto, form=PropertyPhotoForm,
    extra=1, max_num=10, can_delete=True
)

PropertyPeriodFormSet = inlineformset_factory(
    Property, PropertyPeriod, form=PropertyPeriodForm,
    extra=1, max_num=3, can_delete=True
)

class PropertySearchForm(forms.Form):
    """
    Formulário para pesquisa de imóveis.
    """
    location = forms.CharField(
        label='Localização', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Cidade, estado ou CEP'})
    )
    start_date = forms.DateField(
        label='Data de início',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='Data de término',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    min_price = forms.DecimalField(
        label='Preço mínimo',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'min': '0', 'step': '0.01'})
    )
    max_price = forms.DecimalField(
        label='Preço máximo',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'min': '0', 'step': '0.01'})
    )
