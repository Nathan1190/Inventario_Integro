from django.urls import path
from .views import *

app_name = "bien_detalle"

urlpatterns = [
    path("<str:nombre_bien>/<int:objeto_gasto_id>/<int:categoria_id>/<int:subcategoria_id>/", BienDetalleList.as_view(), name="desagrupado"),
    path("bien/<int:pk>/editar/",BienDetalleEdit.as_view(),name="editar"),
    path('export/pdfv/<str:nombre_bien>/<int:objeto_gasto_id>/<int:categoria_id>/<int:subcategoria_id>/', export_inventario_pdfv, name="inventario_pdfv"),  
    path('export/pdfh/<str:nombre_bien>/<int:objeto_gasto_id>/<int:categoria_id>/<int:subcategoria_id>/', export_inventario_pdfh, name="inventario_pdfh"),
    path("bien/<int:pk>/eliminar/", BienDetalleDelete.as_view(), name="eliminar"),
]
