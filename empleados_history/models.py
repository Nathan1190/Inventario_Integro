from django.db import models
from empleados.models import Empleados
from django.conf import settings

class Empleados_History(models.Model):
    empleado = models.ForeignKey(
        Empleados,
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

    nombre_cambio                 = models.CharField(max_length=50)
    cargo_cambio                  = models.CharField(max_length=90)
    dependencia_cambio            = models.CharField(max_length=80)
    contacto_cambio               = models.CharField(max_length=120)
    correo_inst_cambio            = models.CharField(max_length=100)   
    codigo_empleado_cambio        = models.CharField(max_length=4)     
    activo_cambio                 = models.BooleanField()
    creado_fecha_cambio           = models.DateTimeField()
    fecha_de_modificacion_cambio  = models.DateTimeField()
    eliminado_cambio              = models.BooleanField()

    class Meta:
        db_table = "empleados_history"
        ordering = ["-timestamp"]

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Desconocido"
        return f"Historial de {self.empleado.nombre} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"