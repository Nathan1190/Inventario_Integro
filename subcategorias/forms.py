from django import forms
from .models import Subcategorias

class FormSubcategorias(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model  = Subcategorias
        fields = ["nombre", "descripcion", "categoria"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de la subcategoría"
            }),
            "descripcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese la descripción"
            }),
            "categoria": forms.Select(attrs={
                "class": "form-control"
            }),
        }

class FormSubcategoriasDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["readonly"] = True
            field.widget.attrs["disabled"] = True

    class Meta:
        model  = Subcategorias
        fields = ["nombre", "descripcion", "categoria"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
        }
