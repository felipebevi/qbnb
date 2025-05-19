from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('create/<int:period_id>/', views.reservation_create, name='reservation_create'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('<int:pk>/cancel/', views.reservation_cancel, name='reservation_cancel'),
]
