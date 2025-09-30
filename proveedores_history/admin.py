from django.contrib import admin
from .models import Proveedores_History

@admin.register(Proveedores_History)
class ProveedoresHistoryAdmin(admin.ModelAdmin):
    """
    Panel de administración para el historial de proveedores.
    Muestra una bitácora de cambios aplicados.
    """
    list_display = (
        "id",
        "proveedor",
        "nombre_cambio",
        "telefono_cambio",
        "correo_cambio",
        "activo_cambio",
        "eliminado_cambio",
        "changed_by",
        "timestamp",
    )
    list_filter = ("activo_cambio", "eliminado_cambio", "timestamp")
    search_fields = (
        "proveedor__nombre", "nombre_cambio", "correo_cambio", "telefono_cambio", "changed_by__username"
    )
    ordering = ("-timestamp",)
    readonly_fields = [f.name for f in Proveedores_History._meta.fields]
    date_hierarchy = "timestamp"
