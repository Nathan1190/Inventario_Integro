from django.urls import path
from .views import *

app_name = "roles_history"  

urlpatterns = [
    path('', Roles_HistoryList.as_view(), name="home_roles_history"),  
]
