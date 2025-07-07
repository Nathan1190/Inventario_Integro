# inventario_history/models.py

from django.db import models
from inventario.models import BienNacional
from django.conf import settings

class BienNacionalHistory(models.Model):
    bien = models.ForeignKey(BienNacional, on_delete=models.CASCADE, related_name='historial')
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modificado por"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    # Copia los campos clave del bien
    nombre_bien = models.CharField(max_length=100)
    objeto_gasto = models.CharField(max_length=80, blank=True)
    categoria = models.CharField(max_length=80, blank=True)
    subcategoria = models.CharField(max_length=80, blank=True, null=True)
    numero_modelo = models.CharField(max_length=50, blank=True, null=True)
    manufacturera = models.CharField(max_length=80, blank=True, null=True)
    fabricante = models.CharField(max_length=80, blank=True, null=True)
    proveedor = models.CharField(max_length=120, blank=True, null=True)
    serial = models.CharField(max_length=50, blank=True, null=True)
    numero_inventario = models.CharField(max_length=20)
    unidad_medida = models.CharField(max_length=30, blank=True, null=True)
    ubicacion = models.CharField(max_length=80, blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    costo_compra = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    numero_orden = models.CharField(max_length=60, blank=True, null=True)
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    estado_fisico = models.CharField(max_length=200, blank=True, null=True)
    responsable = models.CharField(max_length=150, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    notas = models.TextField(blank=True, null=True)
    eliminado = models.BooleanField(default=False)
    # Puedes agregar más campos si quieres

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Historial de Bien Nacional"
        verbose_name_plural = "Historial de Bienes Nacionales"

    def __str__(self):
        return f"Historial {self.bien} por {self.changed_by} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
