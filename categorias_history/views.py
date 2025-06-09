from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from roles.mixins import PantallaRequiredMixin

class Categorias_HistoryList(PantallaRequiredMixin, ListView):
    template_name        = 'Historiales/Categorias_History/CRUD/index.html'
    queryset             = Categorias_History.objects.all().order_by('id')
    context_object_name  = "Categorias_History"
    pantalla_required    = '0013'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)          
        return ctx