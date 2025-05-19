from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Property, PropertyPhoto, PropertyPeriod
from .forms import PropertyForm, PropertyPhotoFormSet, PropertyPeriodFormSet, PropertySearchForm

def property_list(request):
    """
    View para listar imóveis com filtros de pesquisa.
    """
    properties = Property.objects.all().order_by('-created_at')
    form = PropertySearchForm(request.GET or None)
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if location:
            properties = properties.filter(
                Q(city__icontains=location) | 
                Q(state__icontains=location) | 
                Q(zip_code__icontains=location)
            )
        
        if min_price:
            properties = properties.filter(price__gte=min_price)
        
        if max_price:
            properties = properties.filter(price__lte=max_price)
        
        if start_date and end_date:
            # Filtrar imóveis com períodos disponíveis entre as datas selecionadas
            properties = properties.filter(
                periods__start_date__lte=end_date,
                periods__end_date__gte=start_date,
                periods__is_reserved=False
            ).distinct()
    
    paginator = Paginator(properties, 9)  # 9 imóveis por página
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    
    context = {
        'properties': properties,
        'form': form,
    }
    return render(request, 'properties/property_list.html', context)

def property_detail(request, slug):
    """
    View para exibir detalhes de um imóvel específico.
    """
    property = get_object_or_404(Property, slug=slug)
    photos = property.photos.all()
    periods = property.periods.filter(is_reserved=False)
    
    context = {
        'property': property,
        'photos': photos,
        'periods': periods,
    }
    return render(request, 'properties/property_detail.html', context)

@login_required
def property_create(request):
    """
    View para criar um novo imóvel com fotos e períodos.
    """
    if not request.user.profile.is_advertiser:
        messages.error(request, 'Você precisa ser um anunciante para cadastrar imóveis.')
        return redirect('profile')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            
            # Processar formset de fotos
            photo_formset = PropertyPhotoFormSet(request.POST, request.FILES, instance=property)
            if photo_formset.is_valid():
                photo_formset.save()
            
            # Processar formset de períodos
            period_formset = PropertyPeriodFormSet(request.POST, instance=property)
            if period_formset.is_valid():
                period_formset.save()
            
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            
            # Enviar e-mail de confirmação
            subject = 'Imóvel cadastrado com sucesso!'
            html_message = render_to_string('emails/property_created.html', {
                'user': request.user,
                'property': property
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = request.user.email
            
            try:
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            except Exception as e:
                # Log do erro, mas não impede o cadastro
                print(f"Erro ao enviar e-mail: {e}")
            
            return redirect('property_detail', slug=property.slug)
    else:
        form = PropertyForm()
        photo_formset = PropertyPhotoFormSet()
        period_formset = PropertyPeriodFormSet()
    
    context = {
        'form': form,
        'photo_formset': photo_formset,
        'period_formset': period_formset,
    }
    return render(request, 'properties/property_form.html', context)

@login_required
def property_update(request, slug):
    """
    View para atualizar um imóvel existente.
    """
    property = get_object_or_404(Property, slug=slug)
    
    # Verificar se o usuário é o proprietário
    if property.owner != request.user and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para editar este imóvel.')
        return redirect('property_detail', slug=property.slug)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            property = form.save()
            
            # Processar formset de fotos
            photo_formset = PropertyPhotoFormSet(request.POST, request.FILES, instance=property)
            if photo_formset.is_valid():
                photo_formset.save()
            
            # Processar formset de períodos
            period_formset = PropertyPeriodFormSet(request.POST, instance=property)
            if period_formset.is_valid():
                period_formset.save()
            
            messages.success(request, 'Imóvel atualizado com sucesso!')
            return redirect('property_detail', slug=property.slug)
    else:
        form = PropertyForm(instance=property)
        photo_formset = PropertyPhotoFormSet(instance=property)
        period_formset = PropertyPeriodFormSet(instance=property)
    
    context = {
        'form': form,
        'photo_formset': photo_formset,
        'period_formset': period_formset,
        'property': property,
    }
    return render(request, 'properties/property_form.html', context)

@login_required
def property_delete(request, slug):
    """
    View para excluir um imóvel.
    """
    property = get_object_or_404(Property, slug=slug)
    
    # Verificar se o usuário é o proprietário
    if property.owner != request.user and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para excluir este imóvel.')
        return redirect('property_detail', slug=property.slug)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Imóvel excluído com sucesso!')
        return redirect('property_list')
    
    context = {
        'property': property,
    }
    return render(request, 'properties/property_confirm_delete.html', context)
