from django.contrib import admin
from .models import BienNacional, Manufacturera, Compania, Fabricante, StockBien

@admin.register(BienNacional)
class BienNacionalAdmin(admin.ModelAdmin):
    list_display = (
        'numero_inventario',
        'nombre_bien',
        'objeto_gasto',
        'categoria',
        'subcategoria',
        'responsable',
        'ubicacion',
        'fecha_compra',
        'costo_compra',
        'eliminado',
        'creado',
        'modificado',
    )
    list_filter = ('categoria', 'subcategoria', 'eliminado', 'creado', 'modificado')
    search_fields = ('nombre_bien', 'numero_inventario', 'serial', 'numero_orden', 'numero_factura')
    ordering = ('-creado',)
    date_hierarchy = 'creado'
    readonly_fields = ('creado', 'modificado')

@admin.register(Manufacturera)
class ManufactureraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'contacto', 'telefono')
    search_fields = ('nombre', 'contacto')
    ordering = ('nombre',)

@admin.register(Compania)
class CompaniaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'contacto', 'telefono')
    search_fields = ('nombre', 'contacto')
    ordering = ('nombre',)

@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(StockBien)
class StockBienAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_bien',
        'objeto_gasto',
        'categoria',
        'subcategoria',
        'cantidad_minima',
        'cantidad_restante',
        'total_asignado'
    )
    list_filter = ('categoria', 'subcategoria')
    search_fields = ('nombre_bien',)
    ordering = ('nombre_bien',)
