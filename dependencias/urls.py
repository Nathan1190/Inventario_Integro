from django.urls import path
from .views import *

app_name = "dependencias"  

urlpatterns = [
    path('', DependenciasList.as_view(), name="home_dependencias"),  
    path('CRUD/add.html', DependenciasCreate.as_view(), name="dependencias_create"),  
    path('CRUD/edit.html/<int:pk>', DependenciasEdit.as_view(), name="dependencias_edit"),  
    path('CRUD/delete.html/<int:pk>', DependenciasDelete.as_view(), name="dependencias_delete"), 
]
