from django.contrib import admin
from .models import AsignacionBien

@admin.register(AsignacionBien)
class AsignacionBienAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Asignaciones de Bienes.
    Permite ver todos los estados, responsables y archivos PDF de firmas.
    """
    list_display = (
        "id",
        "bien",
        "responsable",
        "estado",
        "fecha_asignacion",
        "fecha_aceptado",
        "fecha_firma",
        "fecha_descargo",
        "asignado_por",
    )
    list_filter = ("estado", "fecha_asignacion", "fecha_firma", "fecha_descargo")
    search_fields = ("bien__numero_inventario", "responsable__nombres", "responsable__apellidos")
    date_hierarchy = "fecha_asignacion"
    readonly_fields = ("fecha_asignacion", "fecha_aceptado", "fecha_firma", "fecha_descargo")
