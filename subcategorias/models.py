from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from core.middleware import get_current_user
from django.dispatch import receiver
from categorias.models import Categorias

class Subcategorias(models.Model):
    nombre = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    descripcion = models.CharField(
        max_length=120,
        blank=True
    )
    categoria = models.ForeignKey(
        Categorias,
        on_delete=models.PROTECT,
        related_name="subcategorias"
    )
    creado_fecha = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "subcategorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        super().save(*args, **kwargs)

@receiver(post_save, sender=Subcategorias)
def crear_historial_subcategoria(sender, instance, created, **kwargs):
    from subcategorias_history.models import Subcategorias_History
    user = get_current_user()
    Subcategorias_History.objects.create(
        subcategoria                  = instance,
        changed_by                    = user,
        nombre_cambio                 = instance.nombre,
        descripcion_cambio            = instance.descripcion,
        categoria_cambio              = instance.categoria,
        creado_fecha_cambio           = instance.creado_fecha,
        fecha_de_modificacion_cambio  = instance.fecha_de_modificacion,
        eliminado_cambio              = instance.eliminado,
    )
