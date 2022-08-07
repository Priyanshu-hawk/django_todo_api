from django.urls import path, include
from . import views

urlpatterns = [
    path('api', views.TodoListAppView.as_view()),
    path('api/<int:todo_id>/', views.TodoDetailApiView.as_view()),
]