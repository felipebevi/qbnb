from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import CustomUserCreationForm, UserProfileForm

def register(request):
    """
    View para registro de novos usuários com perfil personalizado.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticar e fazer login do usuário após o registro
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            login(request, user)
            
            # Enviar e-mail de boas-vindas
            subject = 'Bem-vindo ao QuotasBNB!'
            html_message = render_to_string('emails/welcome_email.html', {'user': user})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            
            try:
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            except Exception as e:
                # Log do erro, mas não impede o cadastro
                print(f"Erro ao enviar e-mail: {e}")
            
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo ao QuotasBNB.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """
    View para visualização e edição do perfil do usuário.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)

def home(request):
    """
    View para a página inicial.
    """
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """
    View para o painel do usuário.
    """
    # Obter reservas para imóveis do usuário (como anunciante)
    advertiser_reservations = []
    if request.user.profile.is_advertiser:
        from reservations.models import Reservation
        advertiser_reservations = Reservation.objects.filter(
            period__property__owner=request.user
        ).order_by('-created_at')
    
    context = {
        'advertiser_reservations': advertiser_reservations,
    }
    return render(request, 'accounts/dashboard.html', context)
