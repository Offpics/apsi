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
    ProjectTempDetailView,
    ProjectPhaseCreateView,
    ProjectPhaseDetailView,
    ProjectPhaseUpdateView,
    WorkerProjectPhaseDetailView,
    ManagerEndProjectPhase,
    WorkerSummaryView,
)

urlpatterns = [
    # Home page.
    path("", home, name="project-home"),
    # Projects ListView.
    path("projects/", MyProjectsListView.as_view(), name="project-list"),
    path(
        "project/<int:project_pk>/",
        ProjectTempDetailView.as_view(),
        name="project-detail-temp",
    ),
    path(
        "project/<int:project_pk>/createphase/",
        ProjectPhaseCreateView.as_view(),
        name="projectphase-create",
    ),
    path(
        "projectphase/<int:projectphase_pk>/",
        ProjectPhaseDetailView.as_view(),
        name="projectphase-detail",
    ),
    # Projects DetailView.
    path(
        "projects/<int:project_pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projectphase/<int:projectphase_pk>/all/",
        ProjectPhaseDetailView.as_view(),
        {"all": True, "table_view": True},
        name="projectphase-detail-all",
    ),
    path(
        "projectphase/<int:projectphase_pk>/<int:month>/<int:year>/",
        ProjectPhaseDetailView.as_view(),
        {"table_view": True},
        name="projectphase-date-table",
    ),
    path(
        "projects/<int:projectphase_pk>/calendar/<int:worker_pk>/",
        ProjectPhaseDetailView.as_view(),
        {"calendar_view": True},
        name="worker-projectphase-calendar",
    ),
    path(
        "projectphase/<int:projectphase_pk>/table/<int:worker_pk>/",
        ProjectPhaseDetailView.as_view(),
        {"table_view": True},
        name="worker-projectphase-table",
    ),
    path(
        "projectphase/<int:projectphase_pk>/<int:task_pk>/",
        ProjectPhaseDetailView.as_view(),
        {"table_view": True},
        name="task-projectphase-table",
    ),
    path(
        "projectphase/<int:projectphase_pk>/<int:worker_pk>/summary/",
        ProjectPhaseDetailView.as_view(),
        {"worker_summary_view": True},
        name="projectphase-worker-summary",
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
    path(
        "projectphase/<int:projectphase_pk>/update/",
        ProjectPhaseUpdateView.as_view(),
        {"update_view": True},
        name="projectphase-update",
    ),
    # Task DetailView.
    path("task/<int:task_pk>/", TaskDetailView.as_view(), name="task-detail"),
    # Task CreateView.
    path(
        "task/new/<int:projectphase_pk>/",
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
        "datepoint/new/<int:projectphase_pk>/<slug:date>/",
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
    path(
        "worker/projectphase/<int:projectphase_pk>/",
        WorkerProjectPhaseDetailView.as_view(),
        name="worker-projectphase-detail",
    ),
    path(
        "bill/<int:projectphase_pk>/", MyPDF.as_view(), name="bill-for-phase"
    ),
    path(
        "projectphase/<int:projectphase_pk>/endprojectphase/",
        ManagerEndProjectPhase.as_view(),
        name="projectphase-end",
    ),
    path(
        "worker/<int:worker_pk>/",
        WorkerSummaryView.as_view(),
        name="worker-summary",
    ),
]
