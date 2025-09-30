from django.contrib import admin
from .models import Asignaciones_History

@admin.register(Asignaciones_History)
class AsignacionesHistoryAdmin(admin.ModelAdmin):
    """
    Panel de administración para historial de Asignaciones.
    Útil para seguimiento de auditoría.
    """
    list_display = (
        "id",
        "asignacion",
        "bien",
        "responsable",
        "estado",
        "cambiado_en",
        "changed_by",
    )
    list_filter = ("estado", "cambiado_en")
    search_fields = ("bien__numero_inventario", "responsable__nombres", "responsable__apellidos")
    date_hierarchy = "cambiado_en"
    readonly_fields = ("cambiado_en",)
