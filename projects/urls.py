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
    ManagerApproveDatePointView,
    WorkerProjectDetailView,
    WorkerDatePointListView,
    home,
    DatePointUpdateView,
    MyPDF,
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
    path(
        "projects/<int:project_pk>/all/",
        ProjectDetailView.as_view(),
        {"all": True, "table_view": True},
        name="project-detail-all",
    ),
    path(
        "projects/<int:project_pk>/<int:month>/<int:year>/",
        ProjectDetailView.as_view(),
        {"table_view": True},
        name="project-date-table",
    ),
    path(
        "projects/<int:project_pk>/calendar/<int:worker_pk>/",
        ProjectDetailView.as_view(),
        {"calendar_view": True},
        name="worker-project-calendar",
    ),
    path(
        "projects/<int:project_pk>/table/<int:worker_pk>/",
        ProjectDetailView.as_view(),
        {"table_view": True},
        name="worker-project-table",
    ),
    path(
        "projects/<int:project_pk>/<int:task_pk>/",
        ProjectDetailView.as_view(),
        {"table_view": True},
        name="task-project-table",
    ),
    # Project DetailView with approved colors for fullcalendar.
    path(
        "projects/<int:project_pk>/<str:approved>/",
        ProjectDetailView.as_view(),
        name="project-detail-approved",
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
        "datepoint/new/<int:project_pk>/<slug:date>/",
        DatePointCreateView.as_view(),
        name="datepoint-create",
    ),
    # DatePoint CreateView from callendar.
    path(
        "datepoint/new/<int:task_pk>/",
        DatePointCreateView.as_view(),
        name="datepoint-create-from-callendar",
    ),
    # DatePoint DetailView.
    path(
        "datepoint/<int:datepoint_pk>/",
        DatePointDetailView.as_view(),
        name="datepoint-detail",
    ),
    path(
        "datepoint/update/<int:datepoint_pk>/",
        DatePointUpdateView.as_view(),
        name="datepoint-update",
    ),
    # List of user's DatePoints within a project.
    path(
        "datepoints/worker/<int:project_pk>/<int:worker_pk>/",
        WorkerDatePointListView.as_view(),
        name="worker-datepoint-list",
    ),
    # List of DatePoint within project in given day.
    path(
        "datepoints/<int:project_pk>/<slug:date>/",
        DatePointListView.as_view(),
        name="datepoint-list",
    ),
    # Approve DatePoint.
    path(
        "datepoint/<int:datepoint_pk>/approve/",
        ManagerApproveDatePointView.as_view(),
        name="datepoint-approve",
    ),
    # Worker ProjectDetailView.
    path(
        "worker/projects/<int:project_pk>/",
        WorkerProjectDetailView.as_view(),
        name="worker-project-detail",
    ),
    path("bill/<int:project_pk>/", MyPDF.as_view(), name="bill"),
]
