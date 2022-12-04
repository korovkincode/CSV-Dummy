from django.urls import path
from . import views

urlpatterns = [
    path('in/', views.login),
    path('out/', views.logout)
]