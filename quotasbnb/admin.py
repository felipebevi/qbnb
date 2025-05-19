from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from properties.models import Property, PropertyPhoto, PropertyPeriod
from reservations.models import Reservation
from accounts.models import UserProfile

# Personalização do Admin
admin.site.site_header = 'QuotasBNB - Administração'
admin.site.site_title = 'QuotasBNB Admin'
admin.site.index_title = 'Painel de Administração'

# Customização do Admin de Usuários
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_advertiser', 'is_client', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'profile__is_advertiser', 'profile__is_client', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    def is_advertiser(self, obj):
        return obj.profile.is_advertiser
    is_advertiser.boolean = True
    is_advertiser.short_description = 'Anunciante'
    
    def is_client(self, obj):
        return obj.profile.is_client
    is_client.boolean = True
    is_client.short_description = 'Cliente'

# Customização do Admin de Imóveis
class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 1
    max_num = 10

class PropertyPeriodInline(admin.TabularInline):
    model = PropertyPeriod
    extra = 1
    max_num = 3

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'city', 'state', 'price', 'created_at')
    list_filter = ('city', 'state', 'created_at')
    search_fields = ('title', 'description', 'address', 'city', 'state', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PropertyPhotoInline, PropertyPeriodInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('owner', 'title', 'slug', 'description', 'price')
        }),
        ('Localização', {
            'fields': ('address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# Customização do Admin de Reservas
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property_info', 'period_dates', 'confirmed', 'created_at')
    list_filter = ('confirmed', 'created_at', 'period__property__city')
    search_fields = ('user__email', 'period__property__title', 'period__property__city')
    readonly_fields = ('created_at',)
    
    def property_info(self, obj):
        return obj.period.property.title
    property_info.short_description = 'Imóvel'
    
    def period_dates(self, obj):
        return f"{obj.period.start_date} até {obj.period.end_date}"
    period_dates.short_description = 'Período'

# Registrar os modelos customizados
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Reservation, ReservationAdmin)
