from django.urls import path
from .views import *

app_name = "proveedores_history"  

urlpatterns = [
    path('', Proveedores_HistoryList.as_view(), name="home_proveedores_history"),  
]
