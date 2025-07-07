from django.urls import path
from .views import *

app_name = "categorias"  

urlpatterns = [
    path('', CategoriasList.as_view(), name="home_categorias"),  
    path('CRUD/add.html', CategoriasCreate.as_view(), name="categorias_create"),  
    path('CRUD/edit.html/<int:pk>', CategoriasEdit.as_view(), name="categorias_edit"),  
    path('CRUD/delete.html/<int:pk>', CategoriasDelete.as_view(), name="categorias_delete"), 
    path('export/pdf/', export_categorias_pdf, name="categorias_pdf"),
    path("por_objeto_gasto/", categorias_por_objeto_gasto, name="categorias_por_objeto_gasto"),
]
