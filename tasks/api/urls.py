from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view()),
]