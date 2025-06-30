from django.urls import path
from . import views

app_name = 'asignaciones'

urlpatterns = [
    path('', views.AsignacionBienListView.as_view(), name='lista'),
    path('asignar/<int:bien_id>/', views.AsignarBienCreateView.as_view(), name='asignar'),
    path('confirmar-firma/<int:pk>/', views.ConfirmarFirmaView.as_view(), name='confirmar_firma'),
    path('cancelar/<int:pk>/', views.CancelarAsignacionView.as_view(), name='cancelar'),
]