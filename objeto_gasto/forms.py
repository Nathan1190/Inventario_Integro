from django import forms
from .models import ObjetoGasto

class FormObjetoGasto(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model  = ObjetoGasto
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del objeto de gasto (ej. BIENES MUEBLES)"
            }),
            "descripcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese la descripción"
            }),
        }

class FormObjetoGastoDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["readonly"]  = True
            field.widget.attrs["disabled"]  = True

    class Meta:
        model  = ObjetoGasto
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
        }
