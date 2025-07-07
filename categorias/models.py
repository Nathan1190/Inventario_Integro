from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from core.middleware import get_current_user
from django.dispatch import receiver
from objeto_gasto.models import ObjetoGasto

class Categorias(models.Model):
    objeto_gasto = models.ForeignKey(ObjetoGasto, on_delete=models.PROTECT, related_name="categorias")
    nombre = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    descripcion = models.CharField(
        max_length=120,
        blank=True
    )
    creado_fecha = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Convierte a mayúsculas antes de guardar
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        super().save(*args, **kwargs)

@receiver(post_save, sender=Categorias)
def crear_historial_categoria(sender, instance, created, **kwargs):
    from categorias_history.models import Categorias_History
    user = get_current_user()  # tu middleware para el usuario actual

    Categorias_History.objects.create(
        categoria                    = instance,
        changed_by                   = user,
        nombre_cambio                = instance.nombre,
        descripcion_cambio           = instance.descripcion,
        objeto_gasto_cambio          = instance.objeto_gasto,
        creado_fecha_cambio          = instance.creado_fecha,
        fecha_de_modificacion_cambio = instance.fecha_de_modificacion,
        eliminado_cambio             = instance.eliminado,
    )