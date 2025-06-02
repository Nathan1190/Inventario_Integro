# ubicaciones/models.py

from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

class Ubicaciones(models.Model):
    # ─── Validadores comunes ───
    regex_letras_espacios = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
        message='Sólo letras y espacios. Después se convertirá todo a mayúsculas.'
    )
    min2  = MinLengthValidator(2, 'Mínimo 2 caracteres.')
    max80 = MaxLengthValidator(80, 'Máximo 80 caracteres.')

    # ─── Campos ───
    nombre        = models.CharField(
        max_length=120,
        validators=[regex_letras_espacios, min2, max80],
        verbose_name="Nombre"
    )
    descripcion   = models.CharField(
        max_length=120,
        validators=[regex_letras_espacios, min2, max80],
        verbose_name="Descripción"
    )
    activo        = models.BooleanField(default=False, verbose_name="Activo")
    creado_fecha  = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    fecha_de_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    eliminado     = models.BooleanField(default=False, verbose_name="Eliminado")

    class Meta:
        ordering = ['-creado_fecha']
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def clean(self):
        """
        Normaliza `nombre` y `descripcion`: elimina espacios sobrantes y pasa a mayúsculas.
        """
        for field in ['nombre', 'descripcion']:
            val = getattr(self, field, '')
            if isinstance(val, str):
                setattr(self, field, val.strip().upper())

    def save(self, *args, **kwargs):
        # Asegurarnos de limpiar antes de guardar
        self.clean()
        super().save(*args, **kwargs)
