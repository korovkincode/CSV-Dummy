from django.shortcuts import render, redirect
from .models import Users

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		if username == '':
			return render(request, "users/logpage.html", {'errorname': 'Fill in the username.'})
		if password == '':
			return render(request, "users/logpage.html", {'errorpass': 'Fill in the password.'})
		try:
			Users.objects.get(username = username)
		except:
			return render(request, "users/logpage.html", {'errorname': 'There is no account with this username. Try another'})
		try:
			Users.objects.get(username = username, password = password)
		except:
			return render(request, "users/logpage.html", {'errorpass': 'Password is incorrect. Try another'})
		request.session['username'] = username
		request.session['password'] = password
		return redirect('/admin')
	
	return render(request, "users/logpage.html")