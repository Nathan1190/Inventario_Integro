from django.urls import path
from .views import *

app_name = "subcategorias"  

urlpatterns = [
    path('', SubcategoriasList.as_view(), name="home_subcategorias"),  
    path('CRUD/add.html', SubcategoriasCreate.as_view(), name="subcategorias_create"),  
    path('CRUD/edit.html/<int:pk>', SubcategoriasEdit.as_view(), name="subcategorias_edit"),  
    path('CRUD/delete.html/<int:pk>', SubcategoriasDelete.as_view(), name="subcategorias_delete"),
    path('export/pdf/', export_subcategorias_pdf, name="subcategorias_pdf"),  
    path("por_categoria/", subcategorias_por_categoria, name="subcategorias_por_categoria"),
]
