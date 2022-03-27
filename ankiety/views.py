from django.shortcuts import render
from django.http import HttpResponse
from ankiety.tests import TestMainDB
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
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

# return home view
def home(request):
    return render(request, 'ankiety/home.html', {'books': data})


# dev purpose for database testers
def test(request):

    TestMainDB.run()
    return render(request, 'ankiety/test.html')