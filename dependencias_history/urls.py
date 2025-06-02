# dependencias_history/urls.py

from django.urls import path
from .views import Dependencias_HistoryList

app_name = "dependencias_history"

urlpatterns = [
    path('', Dependencias_HistoryList.as_view(), name="home_dependencias_history"),
]
