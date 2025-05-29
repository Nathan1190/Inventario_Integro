from django.urls import path
from .views import *

app_name = "cargos"  

urlpatterns = [
    path('', CargosList.as_view(), name="home_cargos"),  
    path('CRUD/add.html', CargosCreate.as_view(), name="cargos_create"),  
    path('CRUD/edit.html/<int:pk>', CargosEdit.as_view(), name="cargos_edit"),  
    path('CRUD/delete.html/<int:pk>', CargosDelete.as_view(), name="cargos_delete"), 
]
