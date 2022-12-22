from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard/')),
    path('dashboard/', views.dashboard),
    path('scheme/new/', views.newScheme),
    path('scheme/<int:ID>/', views.viewScheme),
    path('scheme/<int:ID>/edit/', views.editScheme),
    path('scheme/<int:ID>/delete', views.deleteScheme)
]