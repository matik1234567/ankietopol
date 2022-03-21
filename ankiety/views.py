from django.shortcuts import render
from django.http import HttpResponse
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
