# dependencias_history/views.py

from django.views.generic import ListView
from roles.mixins import PantallaRequiredMixin
from .models import Dependencias_History

class Dependencias_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Dependencias_History/CRUD/index.html'
    queryset             = Dependencias_History.objects.all().order_by('-timestamp')
    context_object_name  = "Dependencias_History"
    pantalla_required    = '0008'  # Ajusta este código según tus permisos
