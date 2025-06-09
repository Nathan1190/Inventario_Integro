# categorias/admin.py
from django.contrib import admin
from .models import Categorias


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Categorías.
    Muestra el código autogenerado, permite filtrar por eliminado
    y navegar por fechas de creación.
    """
    list_display   = (
        "id",
        "nombre",
        "descripcion",
        "eliminado",
        "creado_fecha",
        "fecha_de_modificacion",
    )
    list_filter    = ("eliminado", "creado_fecha", "fecha_de_modificacion")
    search_fields  = ("nombre", "descripcion")
    ordering       = ("id",)
    date_hierarchy = "creado_fecha"
    readonly_fields = ("creado_fecha", "fecha_de_modificacion")
