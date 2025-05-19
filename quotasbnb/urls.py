from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),  # Garantindo que as URLs do allauth estão incluídas
    path('properties/', include('properties.urls')),
    path('reservations/', include('reservations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
