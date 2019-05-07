from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectDetailView,
    home,
    ProjectListView,
    TaskCreateView
)

urlpatterns = [
    path('', home, name='project-home'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/new/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(),
         name='project-detail'),
    path('projects/task/new/<int:pk>', TaskCreateView.as_view(), name='task-create')
]
