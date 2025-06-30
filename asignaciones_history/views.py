from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from roles.mixins import PantallaRequiredMixin

class Asignaciones_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Asignaciones_History/CRUD/index.html'
    queryset             = Asignaciones_History.objects.all().order_by('fecha_firma')
    context_object_name  = "Asignaciones_History"
    pantalla_required    = '0022'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)          
        return ctx