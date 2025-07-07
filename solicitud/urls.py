from django.urls import path
from .views import SolicitudBienCreateView, SolicitudBienListView, SolicitudBienDetailView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'solicitud'

urlpatterns = [
    path('nueva/', SolicitudBienCreateView.as_view(), name='crear'),
    path('listar/', SolicitudBienListView.as_view(), name='listar'),
    path('<int:pk>/', SolicitudBienDetailView.as_view(), name='detalle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)