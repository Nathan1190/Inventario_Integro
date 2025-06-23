from django import forms
from .models import BienNacional, Manufacturera, Fabricante, Estados, Compania, StockBien
from django.core.exceptions import ValidationError
from datetime import date
import re

def validate_email(value):
    if value and '@' not in value:
        raise ValidationError('El correo debe contener @.')

class CompaniaForm(forms.ModelForm):
    class Meta:
        model = Compania
        fields = ['nombre', 'contacto', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234-5678', 'type': 'tel', 'id': 'id_telefono'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if len(nombre) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre.upper()

    def clean_contacto(self):
        contacto = self.cleaned_data.get('contacto', '')
        if contacto and '@' not in contacto:
            raise ValidationError("Debe ser un correo válido.")
        return contacto

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        return telefono

class ManufactureraForm(forms.ModelForm):
    class Meta:
        model = Manufacturera
        fields = ['nombre', 'contacto', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234-5678', 'type': 'tel', 'id': 'id_telefono'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if len(nombre) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre.upper()

    def clean_contacto(self):
        contacto = self.cleaned_data.get('contacto', '')
        if contacto and '@' not in contacto:
            raise ValidationError("Debe ser un correo válido.")
        return contacto

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        return telefono

class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if len(nombre) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre.upper()

class BienNacionalForm(forms.ModelForm):
    cantidad_minima = forms.IntegerField(
        label="Cantidad mínima para stock",
        min_value=0,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Cantidad mínima para stock"})
    )
    total_bienes = forms.IntegerField(
        label="Total de Bienes a agregar",
        min_value=1,
        required=True,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total de bienes"})
    )
    estado_fisico = forms.ModelMultipleChoiceField(
        queryset=Estados.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control dual-listbox',
            'size': 8
        }),
        label='Etiquetas de Estado:'
    )

    class Meta:
        model = BienNacional
        exclude = [
            'numero_inventario', 'responsable', 'eliminado', 'creado', 'modificado',
            'total_asignado', 'cantidad_restante', 'disponibles'
        ]
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'compania': forms.Select(attrs={'class': 'form-control select2'}),
            'nombre_bien': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Silla'}),
            'categoria': forms.Select(attrs={'class': 'form-control select2'}),
            'subcategoria': forms.Select(attrs={'class': 'form-control select2'}),
            'numero_modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número/modelo'}),
            'manufacturera': forms.Select(attrs={'class': 'form-control select2'}),
            'fabricante': forms.Select(attrs={'class': 'form-control select2'}),
            'proveedor': forms.Select(attrs={'class': 'form-control select2'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de Medida'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej: 2000.00'}),
            'numero_orden': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de orden'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de factura'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['compania'].queryset = Compania.objects.all().order_by('nombre')
        self.fields['manufacturera'].queryset = Manufacturera.objects.all().order_by('nombre')
        self.fields['fabricante'].queryset = Fabricante.objects.all().order_by('nombre')
        self.fields['compania'].empty_label = "Seleccione compañía"
        self.fields['manufacturera'].empty_label = "Seleccione manufacturera"
        self.fields['fabricante'].empty_label = "Seleccione fabricante"

    def clean_nombre_bien(self):
        nombre = self.cleaned_data.get('nombre_bien', '')
        if not nombre or len(nombre) < 2:
            raise ValidationError("Debe ingresar un nombre válido de al menos 2 caracteres.")
        return nombre.upper()

    def clean_numero_modelo(self):
        modelo = self.cleaned_data.get('numero_modelo', '')
        if modelo and len(modelo) < 2:
            raise ValidationError("Si coloca modelo, debe tener al menos 2 caracteres.")
        return modelo

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if imagen.size > 2 * 1024 * 1024:  # 2 MB
                raise ValidationError("La imagen no puede superar los 2MB.")
            ext = imagen.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise ValidationError("Formato de imagen no soportado. Solo jpg, jpeg, png o webp.")
        return imagen


    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is not None and total < 1:
            raise ValidationError("El total debe ser mayor a cero.")
        return total

    def clean_fecha_compra(self):
        fecha = self.cleaned_data.get('fecha_compra')
        if fecha and fecha > date.today():
            raise ValidationError("La fecha de compra no puede ser en el futuro.")
        return fecha

    def clean_costo_compra(self):
        costo = self.cleaned_data.get('costo_compra')
        if costo is not None and costo < 0:
            raise ValidationError("El costo de compra debe ser un valor positivo.")
        return costo

    def clean(self):
        cleaned = super().clean()
        total = cleaned.get('total')
        cantidad_minima = cleaned.get('cantidad_minima')
        if total is not None and cantidad_minima is not None:
            if cantidad_minima > total:
                self.add_error('cantidad_minima', "La cantidad mínima no puede ser mayor que el total.")
        # Más validaciones cruzadas aquí si las necesitas
        return cleaned

