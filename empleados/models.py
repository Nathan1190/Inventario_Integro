# your_app/models.py
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

class Empleados(models.Model):
    # ─── Validadores comunes ───
    # Sólo letras y espacios (luego convertimos a mayúsculas)
    regex_letras_espacios = RegexValidator(
        regex=r'^[A-Za-z\s]+$',
        message='Sólo letras y espacios. Después se convertirá todo a mayúsculas.'
    )
    # Nombre/cargo/dependencia: entre 2 y 80 caracteres
    min2 = MinLengthValidator(2, 'Mínimo 2 caracteres.')
    max80 = MaxLengthValidator(80, 'Máximo 80 caracteres.')

    # Contacto: dígitos, espacios, + y - (e.g. "+504 1234-5678")
    regex_contacto = RegexValidator(
        regex=r'^[0-9+\-\s]+$',
        message='Contacto sólo puede tener dígitos, espacios, + y -.'
    )
    max120 = MaxLengthValidator(120, 'Máximo 120 caracteres.')

    # ─── Campos ───
    nombre = models.CharField(
        max_length=120,
        validators=[regex_letras_espacios, MinLengthValidator(2), MaxLengthValidator(120)]
    )
    cargo = models.CharField(
        max_length=80,
        validators=[regex_letras_espacios, min2, max80]
    )
    dependencia = models.CharField(
        max_length=80,
        validators=[regex_letras_espacios, min2, max80]
    )
    contacto = models.CharField(
        max_length=120,
        validators=[regex_contacto, max120]
    )
    activo = models.BooleanField(default=False)
    creado_fecha = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def clean(self):
        # Este método se llama antes de save() y durante form.is_valid()
        # Normaliza los campos de texto:
        for field in ['nombre', 'cargo', 'dependencia', 'contacto']:
            val = getattr(self, field, '')
            if isinstance(val, str):
                # Strip espacios y convierte a mayúsculas
                setattr(self, field, val.strip().upper())

    def save(self, *args, **kwargs):
        # Asegurarse de limpiar antes de guardar
        self.clean()
        super().save(*args, **kwargs)
