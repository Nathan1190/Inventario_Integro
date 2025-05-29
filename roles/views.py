from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from .mixins import PantallaRequiredMixin

class RolesList(PantallaRequiredMixin, ListView):
    template_name        = 'Roles/CRUD/index.html'
    queryset             = Roles.objects.all().order_by('id')
    context_object_name  = "Roles"
    pantalla_required    = '0000'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormRoles()           
        return ctx
    
    def get_queryset(self):
        # Sólo roles no eliminados, ordenados por id
        return Roles.objects.filter(eliminado=False).order_by('id')

class RolesCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Roles/CRUD/add.html'  
    model = Roles  
    form_class = FormRoles 
    pantalla_required = '0000'
    success_url = reverse_lazy('roles:home_roles')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class RolesEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Roles/CRUD/edit.html'  
    model = Roles  
    form_class = FormRoles
    pantalla_required = '0000'
    success_url = reverse_lazy('roles:home_roles')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class RolesDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Roles/CRUD/delete.html'
    model              = Roles
    form_class         = FormRolesDELETE
    pantalla_required  = '0000'
    success_url        = reverse_lazy('roles:home_roles') 

    def post(self, request, pk):
        rol = get_object_or_404(Roles, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)
    
    