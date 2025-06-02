from django.urls import path
from .views import *

app_name = "ubicaciones"  

urlpatterns = [
    path('', UbicacionesList.as_view(), name="home_ubicaciones"),  
    path('CRUD/add.html', UbicacionesCreate.as_view(), name="ubicaciones_create"),  
    path('CRUD/edit.html/<int:pk>', UbicacionesEdit.as_view(), name="ubicaciones_edit"),  
    path('CRUD/delete.html/<int:pk>', UbicacionesDelete.as_view(), name="ubicaciones_delete"), 
]
