from django.urls import path
from .views import *

app_name = "empleados_history"  

urlpatterns = [
    path('', Empleados_HistoryList.as_view(), name="home_empleados_history"),  
]
