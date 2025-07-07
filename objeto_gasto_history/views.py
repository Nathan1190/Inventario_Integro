from django.views.generic import ListView
from .models import ObjetoGasto_History
from roles.mixins import PantallaRequiredMixin

class ObjetoGasto_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Objeto_Gasto_History/CRUD/index.html'
    queryset             = ObjetoGasto_History.objects.all().order_by('id')
    context_object_name  = "Objeto_Gasto_History"
    pantalla_required    = '0025'  

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
