from django.contrib import admin
from django.urls import path
from review import views1

urlpatterns = [
    path('', views1.index, name='home'),
]
