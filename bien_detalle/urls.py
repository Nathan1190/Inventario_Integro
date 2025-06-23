from django.urls import path
from .views import BienDetalleList

app_name = "bien_detalle"

urlpatterns = [
    path(
        "<str:nombre_bien>/<int:categoria_id>/<int:subcategoria_id>/",
        BienDetalleList.as_view(),
        name="desagrupado"
    ),
]
