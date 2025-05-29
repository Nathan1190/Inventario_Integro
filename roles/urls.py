from django.urls import path
from .views import *

app_name = "roles"  

urlpatterns = [
    path('', RolesList.as_view(), name="home_roles"),  
    path('CRUD/add.html', RolesCreate.as_view(), name="roles_create"),  
    path('CRUD/edit.html/<int:pk>', RolesEdit.as_view(), name="roles_edit"),  
    path('CRUD/delete.html/<int:pk>', RolesDelete.as_view(), name="roles_delete"), 
]
