from django.contrib import admin
from django.urls import path, include
import rest_framework
import todo_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('todos/',include('todo_api.urls'))
]
