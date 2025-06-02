# cargos_history/urls.py

from django.urls import path
from .views import Cargos_HistoryList

app_name = "cargos_history"

urlpatterns = [
    path('', Cargos_HistoryList.as_view(), name="home_cargos_history"),
]
