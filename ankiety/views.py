from django.shortcuts import render
from django.http import HttpResponse
#from ankiety.tests import TestMainDB
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from ankiety.static.py.DBManager import DBManager
# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'ankiety/login.html'
    fields = '_all_'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
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

formItems = [
    {
      "id": 0,
      "type": "c",
      "description": "headline of item 1",
      "value": ["description of checkbox 1", "description of checkbox 2"],
      "name": "shshhs",
      "placeholder": "",
      "is_req": "T"
    },
    {
      "id": 1,
      "type": "t",
      "description": "headline of item 2",
      "value": "placeholder(optionally)",
      "name": "shshhs",
      "placeholder": "",
      "is_req": "T"
    },
    {
      "id": 2,
      "type": "r",
      "description": "headline of item 3",
      "value": ["description of radio 1", "description of radio 2"],
      "name": "shshhs",
      "placeholder": "",
      "is_req": "F"
    },
    {
      "id": 3,
      "type": "s",
      "description": "headline of item 4",
      "value": [0, 5],
      "name": "shshhs",
      "placeholder": "",
      "is_req": "T"
    },
    {
      "id": 4,
      "type": "n",
      "description": "headline of item 4",
      "value": [5, 80],
      "name": "shshhs",
      "placeholder": "",
      "is_req": "T"
    }
  ]

# return home view
def home(request):
    return render(request, 'ankiety/home.html', {'books': data})

# poll creator
def create_poll(request):
    if request.method == "POST":
        DBManager.convert_to_json(request.POST, 1)  # user id
    return render(request, 'ankiety/poll_create.html')

# poll view
def poll(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'ankiety/poll.html', {'polls': formItems})

# dev purpose for database testers
def test(request):

    TestMainDB.run()
    return render(request, 'ankiety/test.html')

# dev purpose test forms
def test_form(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'ankiety/test_form.html')
