from django.db import models
from proveedores.models import Proveedores
from django.conf import settings

class Proveedores_History(models.Model):
    proveedor = models.ForeignKey(
        Proveedores,
        on_delete=models.CASCADE,
        related_name='historial'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modificado por"
    )
    timestamp = models.DateTimeField(auto_now_add=True)


    nombre_cambio  = models.CharField("Nombre", max_length=60)
    descripcion_cambio = models.CharField(max_length=120)
    telefono_cambio = models.CharField(max_length=120)
    correo_cambio = models.CharField(max_length=100)
    direccion_cambio = models.CharField(max_length=150)
    activo_cambio = models.BooleanField()
    creado_fecha_cambio   = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion_cambio = models.DateTimeField(auto_now=True)
    eliminado_cambio   = models.BooleanField()

    class Meta:
        db_table  = "proveedores_history"
        ordering  = ["-timestamp"]

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Desconocido"
        return f"Historial de {self.proveedor.nombre} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
