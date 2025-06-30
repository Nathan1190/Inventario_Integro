from django import forms
from .models import AsignacionBien

class AsignacionBienForm(forms.ModelForm):
    class Meta:
        model = AsignacionBien
        fields = ['responsable', 'comentario']
        widgets = {
            'responsable': forms.Select(attrs={'class': 'form-select select2'}),
            'comentario': forms.Textarea(attrs={'rows': 2}),
        }
