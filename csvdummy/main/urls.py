from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('scheme/new/', views.newScheme),
    path('scheme/<int:ID>/', views.viewScheme),
]