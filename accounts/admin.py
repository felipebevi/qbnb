from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_is_advertiser', 'get_is_client')
    
    def get_is_advertiser(self, obj):
        return obj.profile.is_advertiser
    get_is_advertiser.short_description = 'Anunciante'
    get_is_advertiser.boolean = True
    
    def get_is_client(self, obj):
        return obj.profile.is_client
    get_is_client.short_description = 'Cliente'
    get_is_client.boolean = True

# Re-registrar o modelo User com a nova classe UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
