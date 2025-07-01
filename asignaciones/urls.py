from django.urls import path
from . import views
from .views import exportar_pendientes_pdf

app_name = 'asignaciones'

urlpatterns = [
    path('', views.AsignacionBienListView.as_view(), name='lista'),
    path('asignar/<int:bien_id>/', views.AsignarBienCreateView.as_view(), name='asignar'),
    path('confirmar-firma/<int:pk>/', views.ConfirmarFirmaView.as_view(), name='confirmar_firma'),
    path('cancelar/<int:pk>/', views.CancelarAsignacionView.as_view(), name='cancelar'),
    path('exportar/pdf/<int:responsable_id>', exportar_pendientes_pdf, name='exportar'),
]