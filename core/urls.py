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
from .views import *
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(url='/dashboard/')),

    path('home/', HomeView.as_view(), name="home"),

    path('loginapp/', include('loginapp.urls')),

    path('roles/',include('roles.urls', namespace='roles')),

    path('empleados/',include('empleados.urls', namespace='empleados')),
    
    path('cargos/',include('cargos.urls', namespace='cargos')),

    path('dependencias/',include('dependencias.urls', namespace='dependencias')),
    
    path('ubicaciones/',include('ubicaciones.urls', namespace='ubicaciones')),

    path('estados/',include('estados.urls', namespace='estados')),
    
    path('proveedores/',include('proveedores.urls', namespace='proveedores')),

    path('categorias/',include('categorias.urls', namespace='categorias')),

    path('inventario/',include('inventario.urls', namespace='inventario')),

    path('subcategorias/',include('subcategorias.urls', namespace='subcategorias')),

    path('bien_detalle/',include('bien_detalle.urls', namespace='bien_detalle')),
    
    path('asignaciones/',include('asignaciones.urls', namespace='asignaciones')),

    path('solicitud/',include('solicitud.urls', namespace='solicitud')),

    path('objeto_gasto/',include('objeto_gasto.urls', namespace='objeto_gasto')),


    path('roles_history/',include('roles_history.urls', namespace='roles_history')),

    path('empleados_history/',include('empleados_history.urls', namespace='empleados_history')),

    path('cargos_history/',include('cargos_history.urls', namespace='cargos_history')),
    
    path('dependencias_history/',include('dependencias_history.urls', namespace='dependencias_history')),

    path('estados_history/',include('estados_history.urls', namespace='estados_history')),

    path('proveedores_history/',include('proveedores_history.urls', namespace='proveedores_history')),

    path('categorias_history/',include('categorias_history.urls', namespace='categorias_history')),

    path('subcategorias_history/',include('subcategorias_history.urls', namespace='subcategorias_history')),

    path('inventario_history/',include('inventario_history.urls', namespace='inventario_history')),
    
    path('asignaciones_history/',include('asignaciones_history.urls', namespace='asignaciones_history')),

    path('objeto_gasto_history/',include('objeto_gasto_history.urls', namespace='objeto_gasto_history')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
