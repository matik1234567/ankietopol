from django.shortcuts import render
from django.http import HttpResponse
from ankiety.tests import TestMainDB
# Create your views here.

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


# dev purpose for database testers
def test(request):

    TestMainDB.run()
    return render(request, 'ankiety/test.html')