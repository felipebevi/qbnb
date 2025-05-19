from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile
from properties.models import Property, PropertyPeriod, PropertyPhoto
from reservations.models import Reservation
import datetime
import tempfile
from PIL import Image
import io

class SystemFlowTestCase(TestCase):
    """
    Testes automatizados para validar o fluxo básico do sistema.
    """
    
    def setUp(self):
        # Criar usuário para testes
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Atualizar o perfil existente em vez de criar um novo
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.is_advertiser = True
        self.profile.is_client = True
        self.profile.save()
        
        # Criar um imóvel para testes
        self.property = Property.objects.create(
            owner=self.user,
            title='Apartamento de Teste',
            description='Um belo apartamento para testes',
            address='Rua dos Testes, 123',
            city='Cidade Teste',
            state='Estado Teste',
            zip_code='12345-678',
            price=100.00
        )
        
        # Criar um período para o imóvel
        self.period = PropertyPeriod.objects.create(
            property=self.property,
            start_date=datetime.date.today() + datetime.timedelta(days=1),
            end_date=datetime.date.today() + datetime.timedelta(days=5)
        )
        
        # Criar uma imagem temporária para testes
        self.image = self.get_temporary_image()
    
    def get_temporary_image(self):
        """Cria uma imagem temporária para testes"""
        image = Image.new('RGB', (100, 100), color='red')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file
    
    def test_home_page(self):
        """Testar acesso à página inicial"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_login_flow(self):
        """Testar fluxo de login"""
        # Acessar página de login
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # Fazer login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',  # Corrigido para usar username em vez de email
            'password': 'testpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_dashboard_access(self):
        """Testar acesso ao dashboard após login"""
        # Fazer login
        self.client.login(username='testuser', password='testpassword123')
        
        # Acessar dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
    
    def test_property_list(self):
        """Testar listagem de imóveis"""
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/property_list.html')
        self.assertContains(response, 'Apartamento de Teste')
    
    def test_property_detail(self):
        """Testar visualização de detalhes do imóvel"""
        response = self.client.get(reverse('property_detail', args=[self.property.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/property_detail.html')
        self.assertContains(response, 'Apartamento de Teste')
    
    def test_property_create(self):
        """Testar fluxo de criação de imóvel"""
        # Fazer login como anunciante
        self.client.login(username='testuser', password='testpassword123')
        
        # Acessar página de criação de imóvel
        response = self.client.get(reverse('property_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/property_form.html')
        
        # Dados para criação do imóvel
        today = datetime.date.today()
        property_data = {
            'title': 'Novo Imóvel de Teste',
            'description': 'Descrição do novo imóvel para testes',
            'address': 'Rua Nova, 456',
            'city': 'Nova Cidade',
            'state': 'Novo Estado',
            'zip_code': '54321-876',
            'price': '200.00',
            
            # Dados para o formset de períodos
            'periods-TOTAL_FORMS': '1',
            'periods-INITIAL_FORMS': '0',
            'periods-MIN_NUM_FORMS': '0',
            'periods-MAX_NUM_FORMS': '1000',
            'periods-0-start_date': (today + datetime.timedelta(days=10)).strftime('%Y-%m-%d'),
            'periods-0-end_date': (today + datetime.timedelta(days=15)).strftime('%Y-%m-%d'),
            
            # Dados para o formset de fotos (sem fotos neste teste)
            'photos-TOTAL_FORMS': '0',
            'photos-INITIAL_FORMS': '0',
            'photos-MIN_NUM_FORMS': '0',
            'photos-MAX_NUM_FORMS': '1000',
        }
        
        # Criar o imóvel
        response = self.client.post(reverse('property_create'), property_data, follow=True)
        
        # Verificar se o imóvel foi criado
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Property.objects.filter(title='Novo Imóvel de Teste').exists())
        
        # Verificar se o período foi criado
        new_property = Property.objects.get(title='Novo Imóvel de Teste')
        self.assertEqual(new_property.periods.count(), 1)
    
    def test_reservation_flow(self):
        """Testar fluxo de reserva"""
        # Criar um segundo usuário para fazer a reserva
        second_user = User.objects.create_user(
            username='client',
            email='client@example.com',
            password='clientpass123'
        )
        
        # Fazer login como cliente
        self.client.login(username='client', password='clientpass123')
        
        # Criar uma reserva
        response = self.client.get(reverse('reservation_create', args=[self.period.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/reservation_form.html')
        
        # Confirmar a reserva
        response = self.client.post(reverse('reservation_create', args=[self.period.id]), {}, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a reserva foi criada
        self.assertTrue(Reservation.objects.filter(user=second_user, period=self.period).exists())
        
        # Verificar se o período foi marcado como reservado
        self.period.refresh_from_db()
        self.assertTrue(self.period.is_reserved)
    
    def test_reservation_list(self):
        """Testar listagem de reservas"""
        # Criar um segundo usuário para fazer a reserva
        second_user = User.objects.create_user(
            username='client2',
            email='client2@example.com',
            password='clientpass123'
        )
        
        # Criar uma reserva para o segundo usuário
        reservation = Reservation.objects.create(
            user=second_user,
            period=self.period
        )
        
        # Fazer login como proprietário do imóvel
        self.client.login(username='testuser', password='testpassword123')
        
        # Acessar lista de reservas
        response = self.client.get(reverse('reservation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/reservation_list.html')
        
    def test_logout(self):
        """Testar logout"""
        # Fazer login
        self.client.login(username='testuser', password='testpassword123')
        
        # Fazer logout (usando POST em vez de GET)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
