from django.db import models
from roles.models import Roles
# Create your models here.
class Roles_History(models.Model):
    rol                     = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='historial')
    timestamp               = models.DateTimeField(auto_now_add=True)

    nombre_cambio           = models.CharField(max_length=50)
    descripcion_cambio      = models.CharField(max_length=160)
    eliminado_cambio        = models.BooleanField()
    usuarios_cambio         = models.TextField(help_text="Lista de usernames, separados por coma")
    pantallas_cambio        = models.TextField(help_text="Lista de identificadores, separados por coma")
    fecha_de_creacion_cambio    = models.DateTimeField()
    fecha_de_modificacion_cambio= models.DateTimeField()

    def __str__(self):
        return f"Historial de {self.rol.nombre} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
