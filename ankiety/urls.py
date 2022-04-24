from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('userpanel/',views.user_panel,name='user_panel'),
    path('', views.home, name='home'),
    path('create-poll/', views.create_poll, name='create_poll'),
    path('poll/<int:pk>/', views.poll, name='poll'),
    path('test', views.test),  # dev purpose
    path('test-form/', views.test_form, name='tf'),  # dev purpose
    path('userpass/', views.userpassview, name='userpass'),
    path('poll-complete/', views.poll_complete, name='poll_complete'),
    path('poll-search/', views.poll_search, name='poll_search'),
    path('poll-manage/', views.poll_manage, name='poll_manage'),
    path('poll-statistics/<int:pk>/', views.poll_statistics, name='poll_statistics'),
    path('register/', views.registerPage, name='register'),
]
