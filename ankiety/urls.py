from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('userpanel/',views.UserPanel,name='UserPanel'),
    path('', views.home, name='home'),
    path('kreator-ankiety/', views.create_poll, name='create_poll'),
    path('ankieta/', views.poll, name='poll'),
    path('test', views.test),  # dev purpose
    path('test-form/', views.test_form, name='tf'),  # dev purpose
    path('userpass/', views.userpassview, name='userpass'),
    path('poll-complete/', views.poll_complete, name='poll_complete'),
]
