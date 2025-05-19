from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<slug:slug>/', views.property_detail, name='property_detail'),
    path('<slug:slug>/update/', views.property_update, name='property_update'),
    path('<slug:slug>/delete/', views.property_delete, name='property_delete'),
]
