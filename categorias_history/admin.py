from django.contrib import admin
from .models import Categorias_History

@admin.register(Categorias_History)
class CategoriasHistoryAdmin(admin.ModelAdmin):
    """
    Panel de administración para historial de cambios en Categorías.
    Permite auditar cambios hechos por los usuarios y ver los snapshots.
    """
    list_display = (
        "id",
        "categoria",
        "nombre_cambio",
        "objeto_gasto_cambio",
        "changed_by",
        "timestamp",
    )
    list_filter = ("eliminado_cambio", "timestamp")
    search_fields = ("nombre_cambio", "descripcion_cambio", "objeto_gasto_cambio", "changed_by__username")
    date_hierarchy = "timestamp"
    readonly_fields = (
        "categoria", "changed_by", "timestamp",
        "nombre_cambio", "descripcion_cambio", "objeto_gasto_cambio",
        "creado_fecha_cambio", "fecha_de_modificacion_cambio", "eliminado_cambio"
    )
