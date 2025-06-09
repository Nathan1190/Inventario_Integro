from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from roles.mixins import PantallaRequiredMixin

class CategoriasList(PantallaRequiredMixin, ListView):
    template_name        = 'Categorias/CRUD/index.html'
    queryset             = Categorias.objects.all().order_by('id')
    context_object_name  = "Categorias"
    pantalla_required    = '0012'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormCategorias()           
        return ctx
    
    def get_queryset(self):
        return Categorias.objects.filter(eliminado=False).order_by('id')

class CategoriasCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Categorias/CRUD/add.html'  
    model = Categorias  
    form_class = FormCategorias
    pantalla_required = '0012'
    success_url = reverse_lazy('categorias:home_categorias')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class CategoriasEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Categorias/CRUD/edit.html'  
    model = Categorias  
    form_class = FormCategorias
    pantalla_required = '0012'
    success_url = reverse_lazy('categorias:home_categorias')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class CategoriasDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Categorias/CRUD/delete.html'
    model              = Categorias
    form_class         = FormCategoriasDELETE
    pantalla_required  = '0012'
    success_url        = reverse_lazy('categorias:home_categorias') 

    def post(self, request, pk):
        rol = get_object_or_404(Categorias, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)