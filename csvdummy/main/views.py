from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .models import DataScheme, DataSchemeColumn, DataSet
from users.models import Users
from datetime import datetime
from time import sleep
from faker import Faker
import csv

faker = Faker()

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
        sleep(2)
        if rows is not None:
            dataset = DataSet(filename=f'scheme_{ID}-rows_{rows}.csv', datascheme=DataScheme.objects.get(scheme_id=ID))
            dataset.save()
            headers = [x.name for x in DataSchemeColumn.objects.filter(datascheme=DataScheme.objects.get(scheme_id=ID))]
            datatypes = [x.datatype for x in DataSchemeColumn.objects.filter(datascheme=DataScheme.objects.get(scheme_id=ID))]
            with open(f'datasets\scheme_{ID}-rows_{rows}.csv', 'w', newline='') as file:
                csvw = csv.writer(file)
                csvw.writerow(headers)
                for line in range(rows):
                    row = []
                    for datatype in datatypes:
                        if datatype == 'Full name':
                            row.append(faker.name())
                        if datatype == 'Job':
                            row.append(faker.job())
                        if datatype == 'Domain name':
                            row.append(faker.domain_name())
                        if datatype == 'Company name':
                            row.append(faker.company())
                        if datatype == 'Address':
                            row.append(faker.address())
                    csvw.writerow(row)
        return HttpResponse(f'scheme_{ID}-rows_{rows}.csv')
    else:
        curScheme = DataScheme.objects.get(scheme_id=ID)
        columns = []
        datasets = []
        cur = 1
        for schemeColumn in list(DataSchemeColumn.objects.filter(datascheme=curScheme)):
            columns.append({'cur': cur, 'name': schemeColumn.name, 'type': schemeColumn.datatype})
            cur += 1
        cur = 1
        for dataset in list(DataSet.objects.filter(datascheme=curScheme)):
            datasets.append({'cur': cur, 'filename': dataset.filename, 'modified': dataset.modified.strftime('%Y-%m-%d')})
            cur += 1
        return render(request, 'main/view-scheme.html', {'now': datetime.now().strftime('%Y-%m-%d'), 'username': request.session['username'], 'columns': columns, 'datasets': datasets, 'scheme_name': curScheme.name, 'scheme_id': curScheme.scheme_id})

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

def deleteScheme(request, ID):
    if request.session.get('username', 0) == 0:
        return redirect('/login')
    scheme = DataScheme.objects.get(scheme_id=ID)
    scheme.delete()
    return redirect('/dashboard')