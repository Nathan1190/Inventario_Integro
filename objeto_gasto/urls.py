from django.urls import path
from .views import *

app_name = "objeto_gasto"

urlpatterns = [
    path('', ObjetoGastoList.as_view(), name="home_objeto_gasto"),
    path('CRUD/add.html', ObjetoGastoCreate.as_view(), name="objeto_gasto_create"),
    path('CRUD/edit.html/<int:pk>', ObjetoGastoEdit.as_view(), name="objeto_gasto_edit"),
    path('CRUD/delete.html/<int:pk>', ObjetoGastoDelete.as_view(), name="objeto_gasto_delete"),
    path('export/pdf/', export_objeto_gasto_pdf, name="objeto_gasto_pdf"),
]
