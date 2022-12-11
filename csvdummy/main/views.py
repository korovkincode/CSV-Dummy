from django.shortcuts import render, redirect
from .models import DataScheme, DataSchemeColumn
from users.models import Users
import csv

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def dashboard(request):
    if request.session.get('username', 0) == 0:
        return redirect('/login')
    curUser = Users.objects.get(username=request.session['username'])
    schemes = list(DataScheme.objects.filter(user=curUser))
    context = []
    num = 1
    for scheme in schemes:
        context.append({'scheme_num': num, 'scheme_id': scheme.scheme_id, 'name': scheme.name, 'user': scheme.user, 'modified': scheme.modified.strftime('%Y-%m-%d')})
        num += 1
    return render(request, 'main/dashboard.html', {'schemes': context, 'username': request.session['username']})

def viewScheme(request, ID):
    if request.session.get('username', 0) == 0:
        return redirect('/login')
    if is_ajax(request):
        rows = int(request.GET.get('rows', None))
        if rows is not None:
            headers = [x.name for x in DataSchemeColumn.objects.filter(datascheme=DataScheme.objects.get(scheme_id=ID))]
            datatypes = [x.datatype for x in DataSchemeColumn.objects.filter(datascheme=DataScheme.objects.get(scheme_id=ID))]
            with open(f'datasets\scheme_{ID}-rows_{rows}.csv', 'w', newline='') as file:
                csvw = csv.writer(file)
                csvw.writerow(headers)
                for line in range(rows):
                    row = []
                    for datatype in datatypes:
                        if datatype == 'Full name':
                            row.append('Cristiano Ronaldo')
                        if datatype == 'Job':
                            row.append('Footballer')
                        if datatype == 'Domain name':
                            row.append('52.84.174.52')
                        if datatype == 'Company name':
                            row.append('CR7')
                        if datatype == 'Address':
                            row.append('Funchal, Portugal')
                    csvw.writerow(row)
    else:
        curScheme = DataScheme.objects.get(scheme_id=ID)
        context = []
        cur = 1
        for schemeColumn in list(DataSchemeColumn.objects.filter(datascheme=curScheme)):
            context.append({'cur': cur, 'name': schemeColumn.name, 'type': schemeColumn.datatype})
            cur += 1
        return render(request, 'main/view-scheme.html', {'username': request.session['username'], 'columns': context, 'scheme_name': curScheme.name, 'scheme_id': curScheme.scheme_id})

def newScheme(request):
    if request.session.get('username', 0) == 0:
        return redirect('/login')
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
    if request.session.get('username', 0) == 0:
        return redirect('/login')
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