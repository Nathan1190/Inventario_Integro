from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from roles.mixins import PantallaRequiredMixin

class Inventario_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Inventario_History/CRUD/index.html'
    queryset             =  BienNacionalHistory.objects.all().order_by('id')
    context_object_name  = "Inventario_History" 
    pantalla_required    = '0018'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)           
        return ctx
