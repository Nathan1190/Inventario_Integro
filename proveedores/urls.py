from django.urls import path
from .views import *

app_name = "proveedores"  

urlpatterns = [
    path('', ProveedoresList.as_view(), name="home_proveedores"),  
    path('CRUD/add.html', ProveedoresCreate.as_view(), name="proveedores_create"),  
    path('CRUD/edit.html/<int:pk>', ProveedoresEdit.as_view(), name="proveedores_edit"),  
    path('CRUD/delete.html/<int:pk>', ProveedoresDelete.as_view(), name="proveedores_delete"), 
]
