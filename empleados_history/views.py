from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from roles.mixins import PantallaRequiredMixin

class Empleados_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Empleados_History/CRUD/index.html'
    queryset             = Empleados_History.objects.all().order_by('id')
    context_object_name  = "Empleados_History" 
    pantalla_required    = '0003'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)           
        return ctx
