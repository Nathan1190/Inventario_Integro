from django.urls import path
from .views import *

app_name = "inventario_history"  

urlpatterns = [
    path('', Inventario_HistoryList.as_view(), name="home_inventario_history"),  
]
