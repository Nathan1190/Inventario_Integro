from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from roles.mixins import PantallaRequiredMixin

class Subcategorias_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Subcategorias_History/CRUD/index.html'
    queryset             = Subcategorias_History.objects.all().order_by('id')
    context_object_name  = "Subcategorias_History"
    pantalla_required    = '0015' 
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)          
        return ctx
