from django.urls import path
from .views import *

app_name = "objeto_gasto_history"

urlpatterns = [
    path('', ObjetoGasto_HistoryList.as_view(), name="home_objeto_gasto_history"),
]
