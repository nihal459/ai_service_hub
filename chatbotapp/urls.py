from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('register', views.register, name='register'),
    path('login_service', views.login_service, name='login_service'),
    path('home', views.home, name='home'),
    path('serviceprofile', views.serviceprofile, name='serviceprofile'),
    path('SignOut', views.SignOut, name='SignOut'),
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
    path('user_home', views.user_home, name='user_home'),
    path('view_service_centers', views.view_service_centers, name='view_service_centers'),
    path('SignOut2', views.SignOut2, name='SignOut2'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_bookings', views.user_bookings, name='user_bookings'),
    path('book/<int:pk>/', views.book, name='book'),
    path('my_bookings', views.my_bookings, name='my_bookings'),
    path('update_booking/<int:pk>/', views.update_booking, name='update_booking'),
    path('user_update_booking/<int:pk>/', views.user_update_booking, name='user_update_booking'),




]