from django import forms
from .models import SolicitudBien, PRIORIDAD_CHOICES
from objeto_gasto.models import ObjetoGasto
from categorias.models import Categorias
from subcategorias.models import Subcategorias
from inventario.models import BienNacional

class SolicitudBienForm(forms.ModelForm):
    class Meta:
        model = SolicitudBien
        fields = ['objeto_gasto', 'categoria', 'subcategoria', 'bien', 'cantidad', 'comentario', 'prioridad', 'memo']

    # Opcional: sobreescribe __init__ para hacer selects dependientes con JS/AJAX si quieres.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si quieres filtrar subcategoría/bien según la categoría seleccionada puedes agregar lógica JS/AJAX en el frontend.
        self.fields['objeto_gasto'].widget.attrs.update({'class': 'form-select select2', 'id': 'id_objeto_gasto'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-select select2', 'id': 'id_categoria'})
        self.fields['subcategoria'].widget.attrs.update({'class': 'form-select select2', 'id': 'id_subcategoria'})
        self.fields['bien'].widget.attrs.update({'class': 'form-select select2'})
        self.fields['comentario'].widget.attrs.update({'placeholder': 'Explica el motivo de la solicitud'})
        self.fields['cantidad'].widget.attrs.update({'min': 1, 'class': 'form-control'})
        self.fields['prioridad'].widget.attrs.update({'class': 'form-select select2'})
        self.fields['memo'].widget.attrs.update({'class': 'form-control'})

        self.fields['objeto_gasto'].queryset = ObjetoGasto.objects.filter(eliminado=False).order_by('nombre')
        self.fields['categoria'].queryset = Categorias.objects.filter(eliminado=False).order_by('nombre')
        self.fields['subcategoria'].queryset = Subcategorias.objects.filter(eliminado=False).order_by('nombre')
        self.fields['bien'].queryset = BienNacional.objects.filter(eliminado=False).order_by('nombre_bien')
        

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 1:
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        return cantidad
    
    def clean_memo(self):
        file = self.cleaned_data.get('memo', False)
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Solo se permiten archivos PDF.")
            if file.size > 10*1024*1024:
                raise forms.ValidationError("El archivo no puede superar los 10MB.")
        return file
