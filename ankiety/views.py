from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from ankiety.tests import TestMainDB
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from ankiety.static.py.DBManager import DBManager
from ankiety.static.py.Parser import Parser
from ankiety.static.py.StatisticsCalculator import StatisticsCalculator
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from ankiety.static.py.Export import Export
import time
import xlsxwriter
import json

# Create your views here.

# Home view
def home(request):
    if request.method == "POST":
        return redirect('poll', request.POST['poll_code'])
    public_polls = DBManager.get_public_newest_polls()
    return render(request, 'ankiety/home.html', {'public_polls': public_polls})


def user_panel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        print(request.POST)
    return render(request, 'ankiety/user_panel.html')


def userpassview(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        print(request.POST)
    return render(request, 'ankiety/userpass.html')


# poll creator
def create_poll(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        DBManager.insert_poll_model(request.POST, 1)  # user id
    return render(request, 'ankiety/poll_create.html')


# poll view
def poll(request, pk):
    if request.method == "POST":
        try:
            DBManager.send_poll_response(request.POST, pk)
        except Exception as ex:
            print('poll response exception')
            return render(request, 'ankiety/error_page.html', {'error': str(ex)})
        return redirect('poll_complete')
    
    try:
        polls = DBManager.get_poll_model(pk)
        return render(request, 'ankiety/poll.html', {'polls': polls})
    except Exception as ex:
        return render(request, 'ankiety/error_page.html', {'error': 'This survey is not available'})


# poll complete
def poll_complete(request):
    return render(request, 'ankiety/poll_complete.html')

# poll manage
def poll_manage(request):
    polls = DBManager.get_user_polls(1)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'ankiety/poll_manage.html', {'polls': polls})

# poll statistics
def poll_statistics(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        poll = DBManager.get_names_types(pk)
        responses = Parser.responses_to_dataframe(pk)
        statistics = StatisticsCalculator.get_basic_measurements(poll, responses)
        return render(request, 'ankiety/poll_statistics.html', {'statistics':  statistics})
    except Exception as ex:
        return render(request, 'ankiety/error_page.html', {'error': str(ex)})

# poll correlation
def poll_correlation(request, pk):
    print(pk)

    polls = DBManager.get_poll_model(pk)
    try:
        if request.method == "POST":
            response = DBManager.get_responses(pk)
            if request.POST['var1_id'] == "" or request.POST['var2_id'] == "":
                return render(request, 'ankiety/poll_correlation.html', {'polls': polls, 'message': 'Error - Question not selected'})

            if request.POST['var1_id'] == request.POST['var2_id']:
                return render(request, 'ankiety/poll_correlation.html', {'polls': polls, 'message': 'Error - The same two questions were chosen'})

            correlation = StatisticsCalculator.get_correlation(polls.items['formItems'], response,
                                                               int(request.POST['var1_id']),
                                                               int(request.POST['var2_id']))
            return render(request, 'ankiety/poll_correlation.html', {'polls': polls, 'correlation': correlation})
        else:
            return render(request, 'ankiety/poll_correlation.html', {'polls': polls})
    except Exception as ex:
        return render(request, 'ankiety/error_page.html', {'error': str(ex)})



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


# login user
def login_page(request):
    if request.user.is_authenticated:
        return redirect('user_panel')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_panel')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'ankiety/login.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('user_panel')
    else:
        form = CreateUserForm()
        # form.TextInput(attrs={'class': 'field-sm'})
        print(form)
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
def logout_user(request):
    logout(request)
    return redirect('home')


# dev purpose for database testers

def test(request):

    DBManager.remove_poll(49, 1)

    if request.method == 'POST':
        return Export.write_xlsx(52)

    poll = DBManager.get_names_types(52)
    responses = Parser.responses_to_dataframe(52)

    stat = StatisticsCalculator.get_basic_measurements(poll, responses)
    #data, title = Parser.parse_to_chart(52)

    print(stat)
    return render(request, 'ankiety/test.html', {'stat':  stat})



# dev purpose test forms
def test_form(request):

    if request.method == "POST":
        DBManager.send_poll_response(request.POST, 41)
    return render(request, 'ankiety/test_form.html')
