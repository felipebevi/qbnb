# Generated by Django 5.2.1 on 2025-05-19 18:18

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('description', models.TextField(verbose_name='Descrição')),
                ('address', models.CharField(max_length=255, verbose_name='Endereço')),
                ('city', models.CharField(max_length=100, verbose_name='Cidade')),
                ('state', models.CharField(max_length=50, verbose_name='Estado')),
                ('zip_code', models.CharField(max_length=20, verbose_name='CEP')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Preço')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL, verbose_name='Proprietário')),
            ],
            options={
                'verbose_name': 'Imóvel',
                'verbose_name_plural': 'Imóveis',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropertyPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Data de início')),
                ('end_date', models.DateField(verbose_name='Data de término')),
                ('is_reserved', models.BooleanField(default=False, verbose_name='Reservado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='properties.property', verbose_name='Imóvel')),
            ],
            options={
                'verbose_name': 'Período do Imóvel',
                'verbose_name_plural': 'Períodos dos Imóveis',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='PropertyPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_photos/%Y/%m/', verbose_name='Imagem')),
                ('caption', models.CharField(blank=True, max_length=100, verbose_name='Legenda')),
                ('is_main', models.BooleanField(default=False, verbose_name='Foto principal')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='properties.property', verbose_name='Imóvel')),
            ],
            options={
                'verbose_name': 'Foto do Imóvel',
                'verbose_name_plural': 'Fotos dos Imóveis',
                'ordering': ['-is_main', 'created_at'],
            },
        ),
    ]
