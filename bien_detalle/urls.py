from django.urls import path
from .views import BienDetalleList, BienDetalleEdit

app_name = "bien_detalle"

urlpatterns = [
    path(
        "<str:nombre_bien>/<int:categoria_id>/<int:subcategoria_id>/",
        BienDetalleList.as_view(),
        name="desagrupado"
    ),
    path(
        "bien/<int:pk>/editar/",
        BienDetalleEdit.as_view(),
        name="editar"
    ),
]
