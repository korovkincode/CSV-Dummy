from django.shortcuts import render, redirect
from .models import DataScheme
from users.models import Users

def dashboard(request):
    curUser = Users.objects.get(username=request.session['username'])
    schemes = [DataScheme.objects.get(user=curUser)]
    return redirect('/dashboard')