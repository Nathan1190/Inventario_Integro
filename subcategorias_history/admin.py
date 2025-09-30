from django.contrib import admin
from .models import Subcategorias_History


@admin.register(Subcategorias_History)
class SubcategoriasHistoryAdmin(admin.ModelAdmin):
    """
    Administración del historial de subcategorías.
    """
    list_display = (
        "id",
        "subcategoria",
        "nombre_cambio",
        "categoria_cambio",
        "changed_by",
        "timestamp",
        "eliminado_cambio"
    )
    list_filter = ("eliminado_cambio", "categoria_cambio", "changed_by")
    search_fields = ("nombre_cambio", "descripcion_cambio", "categoria_cambio", "subcategoria__nombre")
    ordering = ("-timestamp",)
    readonly_fields = (
        "subcategoria",
        "changed_by",
        "timestamp",
        "nombre_cambio",
        "descripcion_cambio",
        "categoria_cambio",
        "creado_fecha_cambio",
        "fecha_de_modificacion_cambio",
        "eliminado_cambio"
    )
