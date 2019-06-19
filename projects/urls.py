from django.urls import path

from .views import (  # TaskDetailView,; WorkerDatePointListView,
    ApproveDatePointView,
    DatePointCreateView,
    DatePointDetailView,
    DatePointUpdateView,
    ManagerEndProject,
    ManagerEndProjectPhase,
    MyProjectsListView,
    # ProjectBill,
    ProjectCreateView,
    # ProjectPhaseBill,
    ProjectPhaseCreateView,
    ProjectPhaseDetailView,
    ProjectPhaseJiraView,
    ProjectPhaseTableAllView,
    ProjectPhaseTableDateView,
    ProjectPhaseWorkerView,
    ProjectPhaseTaskView,
    ProjectPhaseWorkerSummaryView,
    ProjectPhaseCalendarView,
    ProjectPhaseTableDatePointView,
    ProjectPhaseUpdateView,
    ProjectUpdateView,
    TaskCreateView,
    TaskUpdateView,
    WorkerProjectPhaseDetail,
    WorkerSummaryView,
    home,
)

urlpatterns = [
    # Home page.
    path("", home, name="project-home"),
    # Projects ListView.
    path("projects/", MyProjectsListView.as_view(), name="project-list"),
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
    path(
        "projectphase/<int:projectphase_pk>/all/",
        ProjectPhaseTableAllView.as_view(),
        name="projectphase-detail-all",
    ),
    path(
        "projectphase/<int:projectphase_pk>/<int:month>/<int:year>/",
        ProjectPhaseTableDateView.as_view(),
        name="projectphase-date-table",
    ),
    path(
        "projectphase/jira/<int:projectphase_pk>/<int:month>/<int:year>/",
        ProjectPhaseJiraView.as_view(),
        name="projectphase-jira-view",
    ),
    path(
        "projects/<int:projectphase_pk>/calendar/<int:worker_pk>/",
        ProjectPhaseCalendarView.as_view(),
        name="worker-projectphase-calendar",
    ),
    path(
        "projectphase/<int:projectphase_pk>/table/<int:worker_pk>/",
        ProjectPhaseWorkerView.as_view(),
        name="worker-projectphase-table",
    ),
    path(
        "projectphase/<int:projectphase_pk>/<int:task_pk>/",
        ProjectPhaseTaskView.as_view(),
        name="task-projectphase-table",
    ),
    path(
        "projectphase/<int:projectphase_pk>/<int:worker_pk>/summary/",
        ProjectPhaseWorkerSummaryView.as_view(),
        name="projectphase-worker-summary",
    ),
    # Project CreateView.
    path("projects/new/", ProjectCreateView.as_view(), name="project-create"),
    # Project UpdateView.
    path(
        "projects/update/<int:project_pk>/",
        ProjectUpdateView.as_view(),
        {"update_view": True},
        name="project-update",
    ),
    path(
        "projectphase/<int:projectphase_pk>/update/",
        ProjectPhaseUpdateView.as_view(),
        {"update_view": True},
        name="projectphase-update",
    ),
    # Task DetailView.
    # path("task/<int:task_pk>/", TaskDetailView.as_view(), name="task-detail"),
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
    path(
        "datepoints/<int:projectphase_pk>/<int:worker_pk>/<slug:date>/",
        ProjectPhaseTableDatePointView.as_view(),
        name="datepoint-list",
    ),
    # Approve DatePoint.
    path(
        "datepoint/<int:datepoint_pk>/approve/",
        ApproveDatePointView.as_view(),
        name="datepoint-approve",
    ),
    path(
        "worker/projectphase/<int:projectphase_pk>/",
        WorkerProjectPhaseDetail.as_view(),
        name="worker-projectphase-detail",
    ),
    # path(
    #     "bill/projectphase/<int:projectphase_pk>/",
    #     ProjectPhaseBill.as_view(),
    #     name="bill-for-phase",
    # ),
    # path(
    #     "bill/project/<int:project_pk>/",
    #     ProjectBill.as_view(),
    #     name="bill-for-project",
    # ),
    path(
        "projectphase/<int:projectphase_pk>/end/",
        ManagerEndProjectPhase.as_view(),
        name="projectphase-end",
    ),
    path(
        "project/<int:project_pk>/end/",
        ManagerEndProject.as_view(),
        name="project-end",
    ),
    path(
        "worker/<int:worker_pk>/",
        WorkerSummaryView.as_view(),
        name="worker-summary",
    ),
    path(
        "worker/<int:worker_pk>/summary/<int:month>/<int:year>/",
        WorkerSummaryView.as_view(),
        {"worker_summary_view": True},
        name="worker-summary-month",
    ),
]
