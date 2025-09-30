from django.contrib import admin
from .models import SolicitudBien


@admin.register(SolicitudBien)
class SolicitudBienAdmin(admin.ModelAdmin):
    """
    Panel de administración para las solicitudes de bienes.
    """
    list_display = (
        "id",
        "solicitante",
        "dependencia",
        "bien",
        "cantidad",
        "prioridad",
        "estado",
        "fecha_solicitud",
        "fecha_modificacion"
    )
    list_filter = ("estado", "prioridad", "dependencia", "categoria", "subcategoria", "fecha_solicitud")
    search_fields = ("solicitante__nombres", "bien__nombre_bien", "comentario")
    ordering = ("-fecha_solicitud",)
    date_hierarchy = "fecha_solicitud"
    readonly_fields = ("fecha_solicitud", "fecha_modificacion")

    fieldsets = (
        ("Información General", {
            "fields": (
                "solicitante", "dependencia", "memo", "comentario",
                "prioridad", "estado"
            )
        }),
        ("Detalle del Bien", {
            "fields": (
                "objeto_gasto", "categoria", "subcategoria", "bien", "cantidad"
            )
        }),
        ("Tiempos", {
            "fields": ("fecha_solicitud", "fecha_modificacion")
        }),
    )
