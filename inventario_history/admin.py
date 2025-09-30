from django.contrib import admin
from .models import BienNacionalHistory

@admin.register(BienNacionalHistory)
class BienNacionalHistoryAdmin(admin.ModelAdmin):
    """
    Panel de administración para el historial de bienes nacionales.
    Permite auditar los cambios importantes en los bienes registrados.
    """
    list_display = (
        "id",
        "bien",
        "nombre_bien",
        "numero_inventario",
        "ubicacion",
        "estado_fisico",
        "responsable",
        "changed_by",
        "timestamp",
    )
    list_filter = ("eliminado", "timestamp", "categoria", "subcategoria", "ubicacion")
    search_fields = (
        "nombre_bien", "numero_inventario", "estado_fisico",
        "responsable", "ubicacion", "changed_by__username"
    )
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)
    readonly_fields = [f.name for f in BienNacionalHistory._meta.fields]
