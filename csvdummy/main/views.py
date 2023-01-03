from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import DataScheme, DataSchemeColumn, DataSet
from users.models import Users
from datetime import datetime
from time import sleep
from faker import Faker
import csv

faker = Faker()

def is_ajax(request: HttpRequest) -> bool:
	return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def dashboard(request: HttpRequest) -> HttpResponse:
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	curUser = get_object_or_404(Users, username=request.session['username'])
	schemes = list(DataScheme.objects.filter(user=curUser))
	context = []
	num = 1
	for scheme in schemes:
		context.append({'scheme_num': num, 'scheme_id': scheme.scheme_id, 'name': scheme.name, 'user': scheme.user, 'modified': scheme.modified.strftime('%Y-%m-%d')})
		num += 1
	return render(request, 'main/dashboard.html', {'schemes': context, 'username': request.session['username']})

def viewScheme(request: HttpRequest, ID: int) -> HttpResponse:
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	if is_ajax(request):
		rows = request.GET.get('rows', None)
		sleep(2) #To check AJAX request
		if rows is not None:
			rows = int(rows)
			dataset = DataSet(filename=f'scheme_{ID}-rows_{rows}.csv', datascheme=get_object_or_404(DataScheme, scheme_id=ID))
			dataset.save()
			headers = [x.name for x in DataSchemeColumn.objects.filter(datascheme=get_object_or_404(DataScheme, scheme_id=ID))] #Get column names
			datatypes = [x.datatype for x in DataSchemeColumn.objects.filter(datascheme=get_object_or_404(DataScheme, scheme_id=ID))] #Get column datatypes
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
		curScheme = get_object_or_404(DataScheme, scheme_id=ID)
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

def newScheme(request: HttpRequest) -> HttpResponse:
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	if request.method == 'POST':
		curUser = get_object_or_404(Users, username=request.session['username'])
		scheme = DataScheme(name=request.POST['schemeName'], user=curUser)
		scheme.save()
		allColumns = list(zip(request.POST.getlist('columnName')[:-1], request.POST.getlist('datatype')[:-1], request.POST.getlist('order')[:-1])) #Zip data to list
		allColumns.sort(key = lambda el: int(el[2]))
		for columnT in allColumns:
			column = DataSchemeColumn(name=columnT[0], datatype=columnT[1], datascheme=scheme)
			column.save()
		return redirect('/dashboard')
	return render(request, 'main/scheme.html', {'username': request.session['username']})

def editScheme(request: HttpRequest, ID: int) -> HttpResponse:
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	scheme = get_object_or_404(DataScheme, scheme_id=ID)
	if request.method == 'GET':
		context = []
		cur = 0
		for schemeColumn in list(DataSchemeColumn.objects.filter(datascheme=scheme)):
			context.append({'cur': cur, 'name': schemeColumn.name, 'type': schemeColumn.datatype})
			cur += 1
		return render(request, 'main/edit-scheme.html', {'columns': context, 'scheme_name': scheme.name, 'scheme_id': scheme.scheme_id, 'username': request.session['username']})
	
	DataSchemeColumn.objects.filter(datascheme=scheme).delete()
	allColumns = list(zip(request.POST.getlist('columnName')[:-1], request.POST.getlist('datatype')[:-1], request.POST.getlist('order')[:-1])) #Zip data to list
	allColumns.sort(key = lambda el: int(el[2]))
	for columnT in allColumns:
		column = DataSchemeColumn(name=columnT[0], datatype=columnT[1], datascheme=scheme)
		column.save()
	return redirect('/dashboard')

def deleteScheme(request: HttpRequest, ID: int):
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	scheme = get_object_or_404(DataScheme, scheme_id=ID)
	scheme.delete()
	return HttpResponse('200!')
	#return redirect('/dashboard')