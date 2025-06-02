from django.urls import path
from .views import *

app_name = "estados"  

urlpatterns = [
    path('', EstadosList.as_view(), name="home_estados"),  
    path('CRUD/add.html', EstadosCreate.as_view(), name="estados_create"),  
    path('CRUD/edit.html/<int:pk>', EstadosEdit.as_view(), name="estados_edit"),  
    path('CRUD/delete.html/<int:pk>', EstadosDelete.as_view(), name="estados_delete"), 
]
