"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from argparse import Namespace
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
from .views import HomeView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(url='/home/')),

    path('home/', HomeView.as_view(), name="home"),

    path('loginapp/', include('loginapp.urls')),

    path('roles/',include('roles.urls', namespace='roles')),

    path('empleados/',include('empleados.urls', namespace='empleados')),
    
    path('cargos/',include('cargos.urls', namespace='cargos')),

    path('dependencias/',include('dependencias.urls', namespace='dependencias')),
    
    path('ubicaciones/',include('ubicaciones.urls', namespace='ubicaciones')),




    path('roles_history/',include('roles_history.urls', namespace='roles_history')),

    path('empleados_history/',include('empleados_history.urls', namespace='empleados_history')),

    path('cargos_history/',include('cargos_history.urls', namespace='cargos_history')),
]
