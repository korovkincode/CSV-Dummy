from django.shortcuts import render, redirect
from .models import DataScheme, DataSchemeColumn
from users.models import Users

def dashboard(request):
    curUser = Users.objects.get(username=request.session['username'])
    schemes = list(DataScheme.objects.filter(user=curUser))
    context = []
    num = 1
    for scheme in schemes:
        context.append({'scheme_num': num, 'scheme_id': scheme.scheme_id, 'name': scheme.name, 'user': scheme.user, 'modified': scheme.modified.strftime('%Y-%m-%d')})
        num += 1
    return render(request, 'main/dashboard.html', {'schemes': context, 'username': request.session['username']})

def viewScheme(request, ID):
    curScheme = DataScheme.objects.get(scheme_id=ID)
    context = []
    cur = 1
    for schemeColumn in list(DataSchemeColumn.objects.filter(datascheme=curScheme)):
        context.append({'cur': cur, 'name': schemeColumn.name, 'type': schemeColumn.datatype})
        cur += 1
    return render(request, 'main/view-scheme.html', {'username': request.session['username'], 'columns': context, 'scheme_name': curScheme.name, 'scheme_id': curScheme.scheme_id})

def newScheme(request):
    if request.method == 'POST':
        curUser = Users.objects.get(username=request.session['username'])
        scheme = DataScheme(name=request.POST['schemeName'], user=curUser)
        scheme.save()
        allColumns = list(zip(request.POST.getlist('columnName')[:-1], request.POST.getlist('datatype')[:-1], request.POST.getlist('order')[:-1]))
        allColumns.sort(key = lambda el: int(el[2]))
        for columnT in allColumns:
            column = DataSchemeColumn(name=columnT[0], datatype=columnT[1], datascheme=scheme)
            column.save()
        return redirect('/dashboard')
    return render(request, 'main/scheme.html', {'username': request.session['username']})

def editScheme(request, ID):
    scheme = DataScheme.objects.get(scheme_id=ID)
    if request.method == 'GET':
        context = []
        cur = 0
        for schemeColumn in list(DataSchemeColumn.objects.filter(datascheme=scheme)):
            context.append({'cur': cur, 'name': schemeColumn.name, 'type': schemeColumn.datatype})
            cur += 1
        return render(request, 'main/edit-scheme.html', {'columns': context, 'scheme_name': scheme.name, 'scheme_id': scheme.scheme_id, 'username': request.session['username']})
    
    DataSchemeColumn.objects.filter(datascheme=scheme).delete()
    curUser = Users.objects.get(username=request.session['username'])
    allColumns = list(zip(request.POST.getlist('columnName')[:-1], request.POST.getlist('datatype')[:-1], request.POST.getlist('order')[:-1]))
    allColumns.sort(key = lambda el: int(el[2]))
    for columnT in allColumns:
        column = DataSchemeColumn(name=columnT[0], datatype=columnT[1], datascheme=scheme)
        column.save()
    return redirect('/dashboard')