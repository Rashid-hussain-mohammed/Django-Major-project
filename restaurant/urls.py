"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from loginka import views 
from review import views1

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/",views.SignupPage,name='signup'),
    path("login/",views.Loginpage,name='login'),
    path("home/",views.Homepage,name='home'),
    path("logout/",views.LogoutPage,name='logout'),
    path("update/",views1.UpdatePage,name='update'),
    path("MENU/",views1.Add_Menu,name='add_menu'),
    path("solve/",views1.Solve,name='solve'),
    path("homepage/",views.HomePage,name='homepage'),
    path("order/",views.Order,name='order'),
    path("",views.Firstpage,name='firstpage'),
    path("chart/",views1.chart,name='chart'),


]
