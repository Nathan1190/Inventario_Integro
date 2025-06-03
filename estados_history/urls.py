from django.urls import path
from .views import *

app_name = "estados_history"  

urlpatterns = [
    path('', Estados_HistoryList.as_view(), name="home_estados_history"),  
]
