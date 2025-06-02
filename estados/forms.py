from django import forms
from .models import Estados

class FormEstados(forms.ModelForm):
    class Meta:
        model  = Estados
        fields = ("nombre", "descripcion", "color_hex", "eliminado")
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "color_hex": forms.TextInput(attrs={"type": "color", "class": "form-control"}),
            
        }

class FormEstadosDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEstadosDELETE, self).__init__(*args, **kwargs)
        # Hacemos todos los campos de solo lectura
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs['readonly'] = True
            if field_name in ['activo']:
                widget.attrs['disabled'] = True

    class Meta:
        model  = Estados
        fields = ("nombre", "color_hex", "eliminado")
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "color_hex": forms.TextInput(attrs={"type": "color", "class": "form-control"}),
            
        }
