from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from properties.models import PropertyPeriod
from .models import Reservation
from .forms import ReservationForm

@login_required
def reservation_create(request, period_id):
    """
    View para criar uma nova reserva para um período específico.
    """
    period = get_object_or_404(PropertyPeriod, id=period_id)
    
    # Verificar se o período já está reservado
    if period.is_reserved:
        messages.error(request, 'Este período já está reservado.')
        return redirect('property_detail', slug=period.property.slug)
    
    # Verificar se o usuário está tentando reservar seu próprio imóvel
    if period.property.owner == request.user:
        messages.error(request, 'Você não pode reservar seu próprio imóvel.')
        return redirect('property_detail', slug=period.property.slug)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, period=period, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.period = period
            reservation.save()
            
            # Marcar o período como reservado
            period.is_reserved = True
            period.save()
            
            messages.success(request, 'Reserva realizada com sucesso!')
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm(period=period, user=request.user)
    
    context = {
        'form': form,
        'period': period,
        'property': period.property,
    }
    return render(request, 'reservations/reservation_form.html', context)

@login_required
def reservation_detail(request, pk):
    """
    View para exibir detalhes de uma reserva específica.
    """
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Verificar se o usuário é o proprietário da reserva ou do imóvel
    if reservation.user != request.user and reservation.period.property.owner != request.user:
        messages.error(request, 'Você não tem permissão para visualizar esta reserva.')
        return redirect('home')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservations/reservation_detail.html', context)

@login_required
def reservation_list(request):
    """
    View para listar todas as reservas do usuário.
    """
    # Obter reservas feitas pelo usuário (como cliente)
    client_reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    # Obter reservas para imóveis do usuário (como anunciante)
    advertiser_reservations = Reservation.objects.filter(
        period__property__owner=request.user
    ).order_by('-created_at')
    
    context = {
        'client_reservations': client_reservations,
        'advertiser_reservations': advertiser_reservations,
    }
    return render(request, 'reservations/reservation_list.html', context)

@login_required
def reservation_cancel(request, pk):
    """
    View para cancelar uma reserva.
    """
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Verificar se o usuário é o proprietário da reserva
    if reservation.user != request.user:
        messages.error(request, 'Você não tem permissão para cancelar esta reserva.')
        return redirect('reservation_detail', pk=reservation.pk)
    
    if request.method == 'POST':
        # Liberar o período
        period = reservation.period
        period.is_reserved = False
        period.save()
        
        # Excluir a reserva
        reservation.delete()
        
        messages.success(request, 'Reserva cancelada com sucesso!')
        return redirect('reservation_list')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservations/reservation_confirm_cancel.html', context)
