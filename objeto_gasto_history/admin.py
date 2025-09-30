from django.contrib import admin
from .models import ObjetoGasto_History

@admin.register(ObjetoGasto_History)
class ObjetoGastoHistoryAdmin(admin.ModelAdmin):
    """
    Panel de administración para el historial de objetos de gasto.
    Muestra un registro detallado de cambios realizados.
    """
    list_display = (
        "id",
        "objeto_gasto",
        "nombre_cambio",
        "descripcion_cambio",
        "eliminado_cambio",
        "changed_by",
        "timestamp",
    )
    list_filter = ("eliminado_cambio", "timestamp")
    search_fields = (
        "objeto_gasto__nombre", "nombre_cambio", "descripcion_cambio", "changed_by__username"
    )
    ordering = ("-timestamp",)
    readonly_fields = [f.name for f in ObjetoGasto_History._meta.fields]
    date_hierarchy = "timestamp"
