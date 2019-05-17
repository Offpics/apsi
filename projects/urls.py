from django.urls import path

from .views import (
    DatePointCreateView,
    DatePointDetailView,
    DatePointListView,
    MyProjectsListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    home,
)

urlpatterns = [
    # Home page.
    path("", home, name="project-home"),
    # Project model.
    path("projects/", MyProjectsListView.as_view(), name="project-list"),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path("projects/new/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "projects/update/<int:pk>/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    # Task model.
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/new/<int:pk>/", TaskCreateView.as_view(), name="task-create"),
    path(
        "task/update/<int:pk>/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "datepoint/new/<int:pk>/",
        DatePointCreateView.as_view(),
        name="datepoint-create",
    ),
    path(
        "datepoint/<int:pk>/",
        DatePointDetailView.as_view(),
        name="datepoint-detail",
    ),
    path(
        "projects/<int:pk>/<slug:date>/",
        DatePointListView.as_view(),
        name="datepoint-list",
    ),
]
