from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from roles.mixins import PantallaRequiredMixin

class Estados_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Estados_History/CRUD/index.html'
    queryset             = Estados_History.objects.all().order_by('id')
    context_object_name  = "Estados_History" 
    pantalla_required    = '0015'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)           
        return ctx
