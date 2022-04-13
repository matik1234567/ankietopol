from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from ankiety.tests import TestMainDB
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from ankiety.static.py.DBManager import DBManager
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from ankiety.static.py.Export import Export
import time
import xlsxwriter
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



    if request.method == "POST":
        return redirect('poll', request.POST['poll_code'])
    public_polls = DBManager.get_public_newest_polls()
    return render(request, 'ankiety/home.html', {'books': data, 'public_polls': public_polls})


# poll creator
def create_poll(request):
    if request.method == "POST":
        DBManager.insert_poll_model(request.POST, 1)  # user id
    return render(request, 'ankiety/poll_create.html')


# poll view
def poll(request, pk):
    if request.method == "POST":
        try:
            DBManager.send_poll_response(request.POST, pk)
        except Exception as ex:
            return render(request, 'ankiety/error_page.html', {'error': str(ex)})
        return redirect('poll_complete')
    
    try:
        polls = DBManager.get_poll_model(pk)
        return render(request, 'ankiety/poll.html', {'polls': polls})
    except Exception as ex:
        return render(request, 'ankiety/error_page.html', {'error': str(ex)})

# poll complete
def poll_complete(request):
    return render(request, 'ankiety/poll_complete.html')

# poll search
def poll_search(request):
    if request.GET.get("search", default="") != "":
        try:
            polls = DBManager.get_polls_by_title(request.GET)
            return render(request, 'ankiety/poll_search.html', {'polls': polls})
        except Exception as ex:
            return render(request, 'ankiety/error_page.html', {'error': str(ex)})
    else:
        polls = DBManager.get_public_newest_polls()
        return render(request, 'ankiety/poll_search.html', {'polls': polls})


# dev purpose for database testers
def test(request):
    if request.method == 'POST':

        return Export.write_xlsx(50)

    # TestMainDB.run()
    # DBManager.get_polls_by_title("pub tes")
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
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'ankiety/login.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'ankiety/register.html', context)


# logout User
def logoutUser(request):
    logout(request)
    return redirect('home')
