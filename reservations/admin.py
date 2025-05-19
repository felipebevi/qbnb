from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'property_info', 'period_dates', 'confirmed', 'created_at')
    list_filter = ('confirmed', 'created_at')
    search_fields = ('user__email', 'period__property__title')
    
    def property_info(self, obj):
        return obj.period.property.title
    property_info.short_description = 'Imóvel'
    
    def period_dates(self, obj):
        return f"{obj.period.start_date} até {obj.period.end_date}"
    period_dates.short_description = 'Período'
