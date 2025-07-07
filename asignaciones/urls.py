from django.urls import path
from . import views
from .views import exportar_pendientes_pdf, exportar_descargo_pdf

app_name = 'asignaciones'

urlpatterns = [
    path('', views.AsignacionBienListView.as_view(), name='lista'),
    path('asignar/<int:bien_id>/', views.AsignarBienCreateView.as_view(), name='asignar'),
    path('confirmar-proceso/<int:pk>/', views.ProcesoFirmaView.as_view(), name='confirmar_proceso'),
    path('confirmar-firma/<int:pk>/', views.ConfirmarFirmaView.as_view(), name='confirmar_firma'),
    path('cancelar/<int:pk>/', views.CancelarAsignacionView.as_view(), name='cancelar'),
    path('exportar/pdf/<int:responsable_id>', exportar_pendientes_pdf, name='exportar'),
    path('iniciar-descargo/<int:pk>/', views.IniciarDescargoView.as_view(), name='iniciar_descargo'),
    path('confirmar-descargo/<int:pk>/', views.ConfirmarDescargoView.as_view(), name='confirmar_descargo'),
    path('exportar_descargo/pdf/<int:responsable_id>', exportar_descargo_pdf, name='exportar_descargo'),
]