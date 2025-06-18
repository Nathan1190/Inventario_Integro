from django.urls import path
from .views import *

app_name = "subcategorias_history"  

urlpatterns = [
    path('', Subcategorias_HistoryList.as_view(), name="home_subcategorias_history"),
]
