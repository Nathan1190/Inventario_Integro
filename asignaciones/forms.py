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
        
class ConfirmarFirmaForm(forms.ModelForm):
    class Meta:
        model = AsignacionBien
        fields = ['pdf_firmado']

    def clean_pdf_firmado(self):
        file = self.cleaned_data.get('pdf_firmado')
        if not file:
            raise forms.ValidationError("Debes adjuntar el PDF firmado.")
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Solo se permiten archivos PDF.")
        if file.size > 10*1024*1024:
            raise forms.ValidationError("El archivo no puede superar los 10MB.")
        return file
    
class IniciarDescargoForm(forms.ModelForm):
    class Meta:
        model = AsignacionBien
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            }