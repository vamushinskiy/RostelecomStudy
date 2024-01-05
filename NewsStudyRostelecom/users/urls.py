from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='user_index'),
    path('contact_page', views.contact_page, name='contact_page'),
    path('registration', views.registration, name='registration'),
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('profile', views.profile, name='profile'),
    path('edit', views.profile_edit, name='edit'),
    path('password', views.password_edit, name='password'),

]
