# cargos_history/views.py

from django.views.generic import ListView
from roles.mixins import PantallaRequiredMixin
from .models import Cargos_History

class Cargos_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Cargos_History/CRUD/index.html'
    queryset             = Cargos_History.objects.all().order_by('-timestamp')
    context_object_name  = "Cargos_History"
    pantalla_required    = '0007'  
