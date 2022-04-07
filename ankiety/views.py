from django.shortcuts import render , redirect
from django.http import HttpResponse
# from ankiety.tests import TestMainDB
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from ankiety.static.py.DBManager import DBManager


# Create your views here.

def UserPanel(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'ankiety/UserPanel.html')


def userpassview(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'ankiety/userpass.html')


# example
data = [
    {
        'author': 'anonymus',
        'title': 'aaaaaa'
    },
    {
        'author': 'gal anonim',
        'title': 'bbbb'
    }
]

# return home view
def home(request):
    return render(request, 'ankiety/home.html', {'books': data})


# poll creator
def create_poll(request):
    if request.method == "POST":
        DBManager.insert_poll_model(request.POST, 1)  # user id
    return render(request, 'ankiety/poll_create.html')


# poll view
def poll(request):
    if request.method == "POST":
        print(request.POST)
        DBManager.send_poll_response(request.POST, 42)
        return redirect('poll_complete')
    polls = DBManager.get_poll_model(47)
    return render(request, 'ankiety/poll.html', {'polls': polls})

# poll complete
def poll_complete(request):
    return render(request, 'ankiety/poll_complete.html')

# dev purpose for database testers
def test(request):
    #TestMainDB.run()
    DBManager.get_user_polls(1)
    return render(request, 'ankiety/test.html')


# dev purpose test forms
def test_form(request):
    if request.method == "POST":
        DBManager.send_poll_response(request.POST, 42)
    return render(request, 'ankiety/test_form.html')
# login user
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'ankiety/login.html', context)
#logout User
def logoutUser(request):
	logout(request)
	return redirect('home')