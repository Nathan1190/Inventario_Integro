from django.urls import path
from .views import *

app_name = "inventario"  

urlpatterns = [
    path('', BienNacionalList.as_view(), name="home_bienesnacionales"),  
    path('CRUD/add.html', BienNacionalCreate.as_view(), name="biennacional_create"),
    path('export/pdfv/', export_inventario_pdfv, name="inventario_pdfv"),  
    path('export/pdfh/', export_inventario_pdfh, name="inventario_pdfh"),
    path('agregar_mas/', agregar_mas_bienes, name='agregar_mas_bienes'),  
    path("buscar_numero_inventario/", buscar_por_numero_inventario, name="buscar_numero_inventario"),
]
