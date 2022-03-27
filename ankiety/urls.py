from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='home'),name='logout'),
    path('', views.home,name='home'),
    path('test', views.test)  # dev purpose
]