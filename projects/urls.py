from django.urls import path
from .views import (
    home,
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    MyProjectsListView,
    ProjectUpdateView,
    TaskCreateView,
    TaskDetailView,
)

urlpatterns = [
    path('', home, name='project-home'),
    path('projects/', MyProjectsListView.as_view(), name='project-list'),
    path('projects/new/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(),
         name='project-detail'),
    path('projects/<int:pk>/update', ProjectUpdateView.as_view(), name='project-update'),
    # path('myprojects/', MyProjectsListView.as_view(), name='myprojects'),
    path('projects/task/new/<int:pk>', TaskCreateView.as_view(), name='task-create'),
    path('projects/task/<int:pk>', TaskDetailView.as_view(), name='task-detail'),
]
