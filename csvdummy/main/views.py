from django.shortcuts import render, redirect
from .models import DataScheme, DataSchemeColumn
from users.models import Users

def dashboard(request):
    curUser = Users.objects.get(username=request.session['username'])
    schemes = [DataScheme.objects.get(user=curUser)]
    context = []
    for scheme in schemes:
        context.append({'scheme_id': scheme.scheme_id, 'name': scheme.name, 'user': scheme.user, 'modified': scheme.modified.strftime('%Y-%m-%d')})
    return render(request, 'main/dashboard.html', {'schemes': context, 'username': request.session['username']})

def viewScheme(request, ID):
    curScheme = DataScheme.objects.get(scheme_id=ID)
    context = []
    cur = 1
    for schemeColumn in [DataSchemeColumn.objects.get(datascheme=curScheme)]:
        context.append({'cur': cur, 'name': schemeColumn.name, 'type': schemeColumn.datatype})
        cur += 1
    return render(request, 'main/view-scheme.html', {'columns': context, 'scheme_name': curScheme.name, 'scheme_id': curScheme.scheme_id})