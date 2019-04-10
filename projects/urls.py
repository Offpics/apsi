from django.urls import path
from .views import ProjectCreateView, ProjectDetailView, home

urlpatterns = [
    path('projects/new/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/', home, name='project-home')
]
