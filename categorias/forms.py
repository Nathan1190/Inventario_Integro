# categorias/forms.py
from django import forms
from .models import Categorias


class FormCategorias(forms.ModelForm):
    """
    Formulario para crear / editar categorías.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model  = Categorias
        fields = ["nombre", "descripcion", "objeto_gasto"]          
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de la categoría (ej. ELECTRÓNICA)"
            }),
            "descripcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese la descripción"
            }),
            "objeto_gasto": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Seleccione el objeto de gasto"
            }),
        }


class FormCategoriasDELETE(forms.ModelForm):
    """
    Formulario de eliminación (soft-delete).
    Se muestran los campos en solo-lectura y se marca `eliminado=True`.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos todos los campos readonly
        for field_name, field in self.fields.items():
            field.widget.attrs["readonly"]  = True
            field.widget.attrs["disabled"]  = True

    class Meta:
        model  = Categorias
        fields = ["nombre", "descripcion", "objeto_gasto"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "objeto_gasto": forms.Select(attrs={"class": "form-control"}),
            
        }
