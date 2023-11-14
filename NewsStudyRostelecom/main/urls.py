from django.contrib import admin
from django.urls import path
from . import views
import main.views as main_views

handler404 = main_views.custom_404

urlpatterns = [
    path('', views.index, name='home'),
    path('calc/<int:a>/<slug:operation>/<int:b>', views.get_demo),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('content/', views.content, name='content'),

]
