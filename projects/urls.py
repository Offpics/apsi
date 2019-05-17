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
    ApproveDatePointView,
    home,
)

urlpatterns = [
    # Home page.
    path("", home, name="project-home"),
    # Projects ListView.
    path("projects/", MyProjectsListView.as_view(), name="project-list"),
    # Projects DetailView.
    path(
        "projects/<int:project_pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    # Project CreateView.
    path("projects/new/", ProjectCreateView.as_view(), name="project-create"),
    # Project UpdateView.
    path(
        "projects/update/<int:project_pk>/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    # Task DetailView.
    path("task/<int:task_pk>/", TaskDetailView.as_view(), name="task-detail"),
    # Task CreateView.
    path(
        "task/new/<int:project_pk>/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    # Task UpdateView.
    path(
        "task/update/<int:task_pk>/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    # DatePoint CreateView.
    path(
        "datepoint/new/<int:datepoint_pk>/",
        DatePointCreateView.as_view(),
        name="datepoint-create",
    ),
    # DatePoint DetailView.
    path(
        "datepoint/<int:datepoint_pk>/",
        DatePointDetailView.as_view(),
        name="datepoint-detail",
    ),
    # List of DatePoint within project in given day.
    path(
        "projects/<int:project_pk>/<slug:date>/",
        DatePointListView.as_view(),
        name="datepoint-list",
    ),
    path(
        "projects/<int:project_pk>/<slug:date>/<int:datepoint_pk>/approve/",
        ApproveDatePointView.as_view(),
        name="datepoint-approve2",
    ),
    path(
        "datepoint/<int:datepoint_pk>/approve/",
        ApproveDatePointView.as_view(),
        name="datepoint-approve",
    ),
]
