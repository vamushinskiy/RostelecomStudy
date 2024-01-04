from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='user_index'),
    path('contact_page', views.contact_page, name='contact_page'),
    path('registration', views.registration, name='registration'),
]
