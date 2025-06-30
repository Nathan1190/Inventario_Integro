from django.urls import path
from .views import *

app_name = "asignaciones_history"  

urlpatterns = [
    path('', Asignaciones_HistoryList.as_view(), name="home_asignaciones_history"),
]