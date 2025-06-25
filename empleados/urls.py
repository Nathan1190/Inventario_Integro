from django.urls import path
from .views import *

app_name = "empleados"  

urlpatterns = [
    path('', EmpleadosList.as_view(), name="home_empleados"),  
    path('CRUD/add.html', EmpleadosCreate.as_view(), name="empleados_create"),  
    path('CRUD/edit.html/<int:pk>', EmpleadosEdit.as_view(), name="empleados_edit"),  
    path('CRUD/delete.html/<int:pk>', EmpleadosDelete.as_view(), name="empleados_delete"), 
    path('CRUD/bienes_asignados.html/<int:pk>', BienesDeEmpleadoList.as_view(), name="empleado_bienes"),
]
