from django.urls import path
from .views import *

app_name = "categorias_history"  

urlpatterns = [
    path('', Categorias_HistoryList.as_view(), name="home_categorias_history"),
]