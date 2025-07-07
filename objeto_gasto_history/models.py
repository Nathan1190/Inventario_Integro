from django.db import models
from objeto_gasto.models import ObjetoGasto
from django.conf import settings

class ObjetoGasto_History(models.Model):
    objeto_gasto = models.ForeignKey(
        ObjetoGasto,
        on_delete=models.CASCADE,
        related_name="historial"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modificado por"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    # Campos snapshot de Objeto de Gasto
    nombre_cambio                = models.CharField(max_length=80)
    descripcion_cambio           = models.CharField(max_length=120, blank=True)
    creado_fecha_cambio          = models.DateTimeField()
    fecha_de_modificacion_cambio = models.DateTimeField()
    eliminado_cambio             = models.BooleanField()

    class Meta:
        db_table  = "objeto_gasto_history"
        ordering  = ["-timestamp"]
        verbose_name_plural = "Historial de objetos de gasto"

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Sistema"
        return f"Hist/ObjGasto {self.objeto_gasto} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
