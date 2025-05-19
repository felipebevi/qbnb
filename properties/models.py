from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Property(models.Model):
    """
    Modelo para imóveis que podem ser alugados.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name='Proprietário')
    title = models.CharField(max_length=100, verbose_name='Título')
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(verbose_name='Descrição')
    address = models.CharField(max_length=255, verbose_name='Endereço')
    city = models.CharField(max_length=100, verbose_name='Cidade')
    state = models.CharField(max_length=50, verbose_name='Estado')
    zip_code = models.CharField(max_length=20, verbose_name='CEP')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Preço')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Garantir que o slug seja único
            original_slug = self.slug
            count = 1
            while Property.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)
    
    @property
    def main_photo(self):
        """Retorna a primeira foto do imóvel ou None se não houver fotos."""
        return self.photos.first()
    
    @property
    def available_periods(self):
        """Retorna os períodos disponíveis (não reservados) do imóvel."""
        return self.periods.filter(is_reserved=False)


class PropertyPhoto(models.Model):
    """
    Modelo para fotos dos imóveis.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos', verbose_name='Imóvel')
    image = models.ImageField(upload_to='property_photos/%Y/%m/', verbose_name='Imagem')
    caption = models.CharField(max_length=100, blank=True, verbose_name='Legenda')
    is_main = models.BooleanField(default=False, verbose_name='Foto principal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Foto do Imóvel'
        verbose_name_plural = 'Fotos dos Imóveis'
        ordering = ['-is_main', 'created_at']
    
    def __str__(self):
        return f"Foto de {self.property.title}"


class PropertyPeriod(models.Model):
    """
    Modelo para períodos disponíveis para aluguel de um imóvel.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='periods', verbose_name='Imóvel')
    start_date = models.DateField(verbose_name='Data de início')
    end_date = models.DateField(verbose_name='Data de término')
    is_reserved = models.BooleanField(default=False, verbose_name='Reservado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Período do Imóvel'
        verbose_name_plural = 'Períodos dos Imóveis'
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.property.title}: {self.start_date} até {self.end_date}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('A data de início deve ser anterior à data de término.')
