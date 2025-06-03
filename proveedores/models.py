from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator

class Proveedores(models.Model):
    # ─── Validadores comunes ───
    regex_letras_espacios = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s,.]+$',
        message='El nombre sólo puede contener letras, números, espacios y comas.'
    )
    min2  = MinLengthValidator(2, 'Mínimo 2 caracteres.')
    max80 = MaxLengthValidator(80, 'Máximo 80 caracteres.')

    regex_direccion = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s,]+$',
        message='La dirección sólo puede contener letras, números, espacios y comas.'
    )

    regex_contacto = RegexValidator(
        regex=r'^[0-9+\-\s]+$',
        message='Contacto sólo puede tener dígitos, espacios, + y -.'
    )
    max120 = MaxLengthValidator(120, 'Máximo 120 caracteres.')

    regex_email = RegexValidator(
        regex=r'^[\w\.\+\-]+@[\w\-]+\.[A-Za-z]{2,}$',
        message='Ingresa un correo electrónico válido (p.ej. usuario@dominio.com).'
    )

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
    telefono = models.CharField(
        max_length=120,
        validators=[regex_contacto, max120]
    )
    correo = models.CharField(
        "Correo",
        max_length=100,
        validators=[regex_email, EmailValidator(message='Formato de correo inválido.')],
    )
    direccion     = models.CharField(
        max_length=150,
        validators=[regex_direccion, min2, max80],
        verbose_name="Dirección"
    )
    activo        = models.BooleanField(default=False, verbose_name="Activo")
    creado_fecha  = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    fecha_de_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    eliminado     = models.BooleanField(default=False, verbose_name="Eliminado")

    class Meta:
        ordering = ['-creado_fecha']
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def clean(self):
        """
        Normaliza: elimina espacios sobrantes y pasa a mayúsculas.
        """
        for field in ['nombre', 'descripcion', 'direccion']:
            val = getattr(self, field, '')
            if isinstance(val, str):
                setattr(self, field, val.strip().upper())

    def save(self, *args, **kwargs):
        # Asegurarnos de limpiar antes de guardar
        self.clean()
        super().save(*args, **kwargs)
