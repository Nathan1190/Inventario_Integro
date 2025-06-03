from django.db import models
from estados.models import Estados
from django.conf import settings

class Estados_History(models.Model):
    estado = models.ForeignKey(
        Estados,
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
    color_hex_cambio = models.CharField(
        "Color (HEX)",
        max_length=7,
        null=True, blank=True,
    )
    descripcion_cambio = models.CharField(max_length=120)
    eliminado_cambio   = models.BooleanField(default=False)
    creado_en_cambio   = models.DateTimeField(auto_now_add=True)
    actualizado_en_cambio = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = "estados_history"
        ordering  = ["-timestamp"]

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Desconocido"
        return f"Historial de {self.estado.nombre} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
