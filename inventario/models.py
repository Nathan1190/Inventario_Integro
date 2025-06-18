import os   
from django.db import models
from categorias.models import Categorias
from subcategorias.models import Subcategorias         
from ubicaciones.models import Ubicaciones         
from empleados.models import Empleados            
from proveedores.models import Proveedores         
from estados.models import Estados          
from uuid import uuid4
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator, EmailValidator


class Manufacturera(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    contacto = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Compania(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    contacto = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Fabricante(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.nombre

def bien_image_upload_path(instance, filename):
    # Usa el número de inventario si existe, si no un uuid
    ext = filename.split('.')[-1]
    nombre = instance.numero_inventario or str(uuid4())
    filename = f"{nombre}.{ext}"
    # Retorna la ruta relativa desde MEDIA_ROOT
    return os.path.join("assets", "img", "bienes", filename)

class BienNacional(models.Model):
    # Identidad y foto
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to=bien_image_upload_path, null=True, blank=True, verbose_name='Imagen del Bien')

    # Organización
    compania = models.ForeignKey(Compania, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Compañía')
    
    # Información principal
    nombre_bien = models.CharField(max_length=100, verbose_name='Nombre del Bien')
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True, verbose_name='Categoría')
    subcategoria = models.ForeignKey(Subcategorias,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Subcategoría')
    numero_modelo = models.CharField(max_length=50, blank=True, null=True, verbose_name='Número del Modelo')
    manufacturera = models.ForeignKey(Manufacturera, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Manufacturera')
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Fabricante')
    proveedor = models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Proveedor')
    serial = models.CharField(max_length=50, blank=True, null=True, verbose_name='Serial')
    numero_inventario = models.CharField(max_length=20, unique=True, verbose_name='Número de Inventario')
    unidad_medida = models.CharField(max_length=30, null=True, blank=True, verbose_name='Unidad de Medida')
    
    # Ubicación
    ubicacion = models.ForeignKey(Ubicaciones, on_delete=models.SET_NULL, null=True, verbose_name='Ubicación Física')
    
    # Control de cantidades
    cantidad_minima = models.PositiveIntegerField(default=0, verbose_name='Cantidad Mínima', validators=[MinValueValidator(0)])
    total = models.PositiveIntegerField(default=1, verbose_name='Total')
    disponibles = models.PositiveIntegerField(default=1, verbose_name='Disponibles')
    cantidad_restante = models.PositiveIntegerField(default=1, verbose_name='Cantidad de Bien Restante')
    total_asignado = models.PositiveIntegerField(default=0, verbose_name='Total Asignado')
    
    # Control de compra
    fecha_compra = models.DateField(null=True, blank=True, verbose_name='Fecha de Compra')
    costo_compra = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, verbose_name='Costo de Compra')
    numero_orden = models.CharField(max_length=60, blank=True, null=True, verbose_name='Número de Orden')
    numero_factura = models.CharField(max_length=50, null=True, blank=True, verbose_name='Número de Factura')
    
    # Estado y asignación
    estado_fisico = models.ManyToManyField(Estados, blank=True, verbose_name='Etiquetas de Estado')
    responsable = models.ForeignKey(Empleados, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Responsable Actual')

    # Auditoría
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    modificado = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    eliminado = models.BooleanField(default=False, verbose_name='Eliminado')

    notas = models.TextField(blank=True, null=True, verbose_name='Notas')

    def __str__(self):
        return f"{self.numero_inventario} - {self.nombre_bien}"

    class Meta:
        verbose_name_plural = "Bienes Nacionales"
        ordering = ['nombre_bien', 'numero_inventario']





