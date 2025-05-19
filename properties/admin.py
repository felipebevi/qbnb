from django.contrib import admin
from .models import Property, PropertyPhoto, PropertyPeriod

class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 1
    max_num = 10

class PropertyPeriodInline(admin.TabularInline):
    model = PropertyPeriod
    extra = 1
    max_num = 3

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'city', 'state', 'price', 'created_at')
    list_filter = ('city', 'state', 'created_at')
    search_fields = ('title', 'description', 'address', 'city', 'state')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyPhotoInline, PropertyPeriodInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

@admin.register(PropertyPhoto)
class PropertyPhotoAdmin(admin.ModelAdmin):
    list_display = ('property', 'caption', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('property__title', 'caption')

@admin.register(PropertyPeriod)
class PropertyPeriodAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'is_reserved')
    list_filter = ('is_reserved', 'start_date', 'end_date')
    search_fields = ('property__title',)
