from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from roles.mixins import PantallaRequiredMixin

class Proveedores_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Proveedores_History/CRUD/index.html'
    queryset             = Proveedores_History.objects.all().order_by('id')
    context_object_name  = "Proveedores_History" 
    pantalla_required    = '0011'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)           
        return ctx
