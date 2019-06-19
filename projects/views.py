import datetime
import json

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (CreateView, DetailView, ListView, UpdateView,
                                  View)
from django.views.generic.edit import FormMixin

from .forms import (DatePointCreateForm2, ProjectCreateForm,
                    QueryDatepointsForm, WorkerMonthForm)
from .mixins import (UserBelongsToProjectMixin, UserBelongsToTaskMixin,
                     WorkerCanChangeDatePointDetail)
from .models import DatePoint, Project, ProjectPhase, Task

###############################################################################
###############################################################################
###############################################################################
###############################################################################
#                            Project Views
###############################################################################
###############################################################################
###############################################################################
###############################################################################


class ProjectCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):

    form_class = ProjectCreateForm
    template_name = "projects/project_form.html"

    def form_valid(self, form):
        # Get project by id.
        manager = get_object_or_404(User, id=self.request.user.id)

        # Append the form with returned project.
        form.instance.manager = manager

        # Create new Task.
        return super(ProjectCreateView, self).form_valid(form)

    success_message = "Project succesfully created!"

    permission_required = "projects.add_project"


class ProjectUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Project
    pk_url_kwarg = "project_pk"

    form_class = ProjectCreateForm
    template_name = "projects/project_form.html"

    success_message = "Project succesfully updated!"

    permission_required = "projects.change_project"


class MyProjectsListView(
    LoginRequiredMixin, PermissionRequiredMixin, ListView
):
    """ Returns ListView with projects that authenticated user belongs to. """

    template_name = "projects/project_list"
    context_object_name = "projects"

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)

        if user.groups.exists():
            group_name = user.groups.all()[0].name.lower()
            if group_name == "worker":
                queryset = Project.objects.filter(worker=user).order_by(
                    "-ongoing"
                )
            elif group_name == "manager":
                queryset = Project.objects.filter(manager=user).order_by(
                    "-ongoing"
                )
            elif group_name == "client":
                queryset = Project.objects.filter(client=user).order_by(
                    "-ongoing"
                )
            return queryset
        else:
            raise Http404("Cannot view projects.")

    permission_required = "projects.view_project"


###############################################################################
###############################################################################
###############################################################################
###############################################################################
#                            Project Views
###############################################################################
###############################################################################
###############################################################################


class ProjectPhaseUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    UpdateView,
):
    model = ProjectPhase
    pk_url_kwarg = "projectphase_pk"

    fields = ["title"]

    permission_required = "projects.change_projectphase"


class ProjectPhaseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    CreateView,
):
    model = ProjectPhase
    fields = ["title"]

    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        form.instance.project = project

        return super(ProjectPhaseCreateView, self).form_valid(form)

    permission_required = "projects.add_projectphase"


class ProjectPhaseDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    FormMixin,
    DetailView,
):

    model = ProjectPhase
    form_class = QueryDatepointsForm
    pk_url_kwarg = "projectphase_pk"

    def get_form_kwargs(self):
        kwargs = super(ProjectPhaseDetailView, self).get_form_kwargs()

        projectphase = ProjectPhase.objects.get(
            id=self.kwargs["projectphase_pk"]
        )

        kwargs["dates"] = projectphase.get_dates()
        kwargs["initial"] = datetime.datetime.strftime(
            datetime.datetime.now(), "%Y-%m"
        )

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            dates = form.cleaned_data["dates"]
            view = form.cleaned_data["view"]
            projectphase_pk = kwargs["projectphase_pk"]

            if view == "jira_view":
                tmp_url = reverse(
                    "projectphase-jira-view",
                    kwargs={
                        "projectphase_pk": projectphase_pk,
                        "month": dates[5:7],
                        "year": dates[:4],
                    },
                )

            else:
                tmp_url = reverse(
                    "projectphase-date-table",
                    kwargs={
                        "projectphase_pk": projectphase_pk,
                        "month": dates[5:7],
                        "year": dates[:4],
                    },
                )
            return redirect(tmp_url)

    permission_required = "projects.view_projectphase"


class ProjectPhaseTableAllView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_table.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"]
        ).order_by("-worked_date")

        context["datepoint_list"] = queryset

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context


class ProjectPhaseTableDatePointView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_table.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"],
            worker=worker,
            worked_date=self.kwargs["date"],
        )

        context["datepoint_list"] = queryset

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context


class ProjectPhaseWorkerView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_table.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"], worker=worker
        ).order_by("-worked_date")

        context["worker_name"] = worker.username

        context["datepoint_list"] = queryset

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context


class ProjectPhaseWorkerSummaryView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_worker_summary.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"], worker=worker
        ).order_by("-worked_date")

        tasks = Task.objects.filter(project_id=self.kwargs["projectphase_pk"])

        if tasks.exists():
            client_exists = tasks[0].project.project.client.exists()

        tasks_dict = {}
        total_hours = 0

        for task in tasks:
            tasks_dict[f"{task.id}"] = 0

        for datepoint in queryset:
            if client_exists:
                if datepoint.approved_manager and datepoint.approved_client:
                    tasks_dict[f"{datepoint.task.id}"] += datepoint.worked_time
                    total_hours += datepoint.worked_time
            else:
                if datepoint.approved_manager:
                    tasks_dict[f"{datepoint.task.id}"] += datepoint.worked_time
                    total_hours += datepoint.worked_time

        services = []
        for task in tasks:
            services.append(
                {"title": task.title, "hours": tasks_dict[f"{task.id}"]}
            )

        if worker.profile.price_per_hour:
            context["total_hours"] = total_hours
            context["pay"] = total_hours * worker.profile.price_per_hour

        context["services"] = services

        return context


class ProjectPhaseTaskView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_table.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        task = get_object_or_404(Task, id=self.kwargs["task_pk"])
        context["task_title"] = task.title
        queryset = DatePoint.objects.filter(task=task).order_by("-worked_date")

        context["datepoint_list"] = queryset

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context


class ProjectPhaseTableDateView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_table.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"],
            worked_date__month=self.kwargs["month"],
            worked_date__year=self.kwargs["year"],
        ).order_by("-worked_date")

        context["datepoint_list"] = queryset

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context


class ProjectPhaseJiraView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_jira.html"

    def get_context_data(self, **kwargs):

        # Get context.
        context = super().get_context_data(**kwargs)

        group_name = self.request.user.groups.all()[0].name

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"],
            worked_date__month=self.kwargs["month"],
            worked_date__year=self.kwargs["year"],
        ).order_by("-worked_date")

        worked_dates = set()
        workers = set()

        for item in queryset:
            worked_dates.add(
                datetime.datetime.strftime(item.worked_date, "%Y-%m-%d")
            )
            workers.add(item.worker.username)

        worked_dates = sorted(list(worked_dates))
        workers = sorted(list(workers))

        context["worked_dates"] = [item[8:10] for item in worked_dates]

        client_exists = Project.objects.get(
            projectphase__id=self.kwargs["projectphase_pk"]
        ).client.exists()

        workers_list = []
        td_list_js = []

        i = 0
        for worker in workers:
            td_list = []
            for worked_date in worked_dates:
                hours = 0
                queryset = DatePoint.objects.filter(
                    task__project_id=self.kwargs["projectphase_pk"],
                    worked_date=worked_date,
                    worker__username=worker,
                )

                content = ""

                j_change = []
                for datepoint in queryset:
                    hours += datepoint.worked_time
                    content += f"<a href='{reverse('datepoint-detail', kwargs={'datepoint_pk': datepoint.id})}'>"
                    content += (
                        f"<p> {datepoint.title} | {datepoint.worked_time}h "
                    )
                    content += "</a>"
                    if datepoint.approved_manager:
                        content += f"| M: <span id='approved_manager_{datepoint.id}'>✓</span>"
                    else:
                        content += f"| M: <span id='approved_manager_{datepoint.id}'>❌</span>"
                    if client_exists and datepoint.approved_client:
                        content += f"| C: <span id='approved_client_{datepoint.id}'>✓</span>"
                    elif client_exists and not datepoint.approved_client:
                        content += f"| C: <span id='approved_client_{datepoint.id}'>❌</span>"

                    if group_name == "Manager" and datepoint.approved_manager:
                        content += f"<button class='btn btn-danger btn-sm ml-1' id='btn_{datepoint.id}'>-</button></p>"
                    elif (
                        group_name == "Manager"
                        and not datepoint.approved_manager
                    ):
                        content += f"<button class='btn btn-success btn-sm ml-1' id='btn_{datepoint.id}'>+</button></p>"

                    if group_name == "Client" and datepoint.approved_client:
                        content += f"<button class='btn btn-danger btn-sm ml-1' id='btn_{datepoint.id}'>-</button></p>"
                    elif (
                        group_name == "Client"
                        and not datepoint.approved_client
                    ):
                        content += f"<button class='btn btn-success btn-sm ml-1' id='btn_{datepoint.id}'>+</button></p>"

                    j_change.append(datepoint.id)

                td_list.append({"id": f"td_{i}", "hours": hours})
                td_list_js.append(
                    {"id": f"td_{i}", "content": content, "jds": j_change}
                )
                i += 1

            workers_list.append({"username": worker, "td": td_list})

        context["workers"] = workers
        context["workers_list"] = workers_list
        context["td_list_js"] = json.dumps(td_list_js)

        return context


class ProjectPhaseCalendarView(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_calendar.html"

    def get_context_data(self, **kwargs):
        # Get context.
        context = super().get_context_data(**kwargs)

        worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["projectphase_pk"], worker=worker
        ).order_by("-worked_date")

        if self.request.user.groups.all().exists():

            if self.request.user.groups.all()[0].name == "Worker":
                # Create list of dictionaries that is used to populate calendar events.
                datepoints = [
                    {
                        "title": f"{item.task.title} | {item.worked_time}h",
                        # "title": item.worker.username,
                        "start": item.worked_date.strftime("%Y-%m-%d"),
                        "url": reverse(
                            "datepoint-detail",
                            kwargs={"datepoint_pk": item.id},
                        ),
                        # "color": tasks_color[item.task.id],
                    }
                    for item in queryset
                ]
            elif self.request.user.groups.all()[0].name == "Manager":

                datepoints = [
                    {
                        "title": f"{item.task.title} | {item.worked_time}h",
                        # "title": item.worker.username,
                        "start": item.worked_date.strftime("%Y-%m-%d"),
                        "url": reverse(
                            "datepoint-detail",
                            kwargs={"datepoint_pk": item.id},
                        ),
                        "color": "green" if item.approved_manager else "red",
                    }
                    for item in queryset
                ]

            elif self.request.user.groups.all()[0].name == "Client":

                datepoints = [
                    {
                        "title": f"{item.task.title} | {item.worked_time}h",
                        # "title": item.worker.username,
                        "start": item.worked_date.strftime("%Y-%m-%d"),
                        "url": reverse(
                            "datepoint-detail",
                            kwargs={"datepoint_pk": item.id},
                        ),
                        "color": "green" if item.approved_client else "red",
                    }
                    for item in queryset
                ]

        # Create json and add it to context.
        context["datepoints"] = json.dumps(datepoints)

        return context


class WorkerProjectPhaseDetail(ProjectPhaseDetailView):
    template_name = "projects/projectphase_detail_calendar.html"

    def test_func(self):
        if self.request.user.groups.filter(name="Worker").exists():
            return super(WorkerProjectPhaseDetail, self).test_func()
        else:
            return False

    def get_context_data(self, **kwargs):
        """ Populate fullcalendar with datepoints. """

        # Get context.
        context = super().get_context_data(**kwargs)

        # Get DatePoints that belong to current worker.
        queryset = DatePoint.objects.filter(
            worker=self.request.user.id,
            task__project_id=self.kwargs["projectphase_pk"],
        )

        # List of datepoints used to populate fullcallendar.
        datepoints = [
            {
                "title": f"{datepoint.task.title} | {datepoint.worked_time}h",
                "start": datepoint.worked_date.strftime("%Y-%m-%d"),
                "url": reverse(
                    "datepoint-detail", kwargs={"datepoint_pk": datepoint.id}
                ),
            }
            for datepoint in queryset
        ]

        # Create json and add it to the context.
        context["datepoints"] = json.dumps(datepoints)
        context["calendar_view"] = True

        return context


###############################################################################
###############################################################################
###############################################################################
###############################################################################
#                            Task Views
###############################################################################
###############################################################################
###############################################################################


class TaskCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Task
    fields = ["title"]

    def form_valid(self, form):
        # Get project by id.
        projectphase = get_object_or_404(
            ProjectPhase, id=self.kwargs["projectphase_pk"]
        )

        # Append the form with returned project.
        form.instance.project = projectphase

        # Create new Task.
        return super(TaskCreateView, self).form_valid(form)

    success_message = "Task succesfully created!"

    permission_required = "projects.add_task"


# class TaskDetailView(
#     PermissionRequiredMixin, UserBelongsToTaskMixin, DetailView
# ):
#     model = Task
#     pk_url_kwarg = "task_pk"

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context.
#         context = super().get_context_data(**kwargs)

#         # Add in a QuerySet of all the datepoints.
#         datepoint_list = DatePoint.objects.filter(
#             task__id=self.kwargs["task_pk"]
#         )
#         context["datepoint_list"] = datepoint_list

#         datepoints_pks = [item.pk for item in datepoint_list]

#         context["datepoints_pks"] = datepoints_pks

#         return context

#     permission_required = "projects.view_task"


class TaskUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToTaskMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Task
    fields = ["title"]
    pk_url_kwarg = "task_pk"

    success_message = "Task succesfully updated!"

    permission_required = "projects.change_task"


###############################################################################
###############################################################################
###############################################################################
###############################################################################
#                            DatePoint Views
###############################################################################
###############################################################################
###############################################################################


class DatePointCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    SuccessMessageMixin,
    CreateView,
):
    form_class = DatePointCreateForm2
    template_name = "projects/datepoint_form.html"
    pk_url_kwarg = "projectphase_pk"

    def get_form_kwargs(self):
        kwargs = super(DatePointCreateView, self).get_form_kwargs()

        # Add current user to the form.
        kwargs["user"] = self.request.user

        # Add curent project id to the form.
        kwargs["projectphase_pk"] = self.kwargs["projectphase_pk"]

        return kwargs

    def form_valid(self, form):
        form.instance.worker = self.request.user

        form.instance.worked_date = self.kwargs["date"]

        return super(DatePointCreateView, self).form_valid(form)

    success_message = "DatePoint succesfully created!"

    permission_required = "projects.add_datepoint"


# class DatePointCreateView2(
#     PermissionRequiredMixin, SuccessMessageMixin, CreateView
# ):
#     form_class = DatePointCreateForm2
#     template_name = "projects/datepoint_form.html"
#     pk_url_kwarg = "task_pk"

#     def get_form_kwargs(self):
#         kwargs = super(DatePointCreateView, self).get_form_kwargs()

#         # Add current user to the form.
#         kwargs["user"] = self.request.user

#         # Add curent project id to the form.
#         kwargs["task_pk"] = self.kwargs["task_pk"]

#         return kwargs

#     def form_valid(self, form):
#         task = get_object_or_404(Task, id=self.kwargs["task_pk"])
#         form.instance.task = task

#         form.instance.worker = self.request.user

#         return super(DatePointCreateView, self).form_valid(form)

#     success_message = "DatePoint succesfully created!"

#     permission_required = "projects.add_datepoint"


class DatePointDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    DetailView,
):
    model = DatePoint
    pk_url_kwarg = "datepoint_pk"

    permission_required = "projects.view_datepoint"

    def test_func(self):
        # If current user is worker check wheter datepoints is his.
        if self.request.user.groups.filter(name="Worker").exists():
            return DatePoint.objects.filter(
                worker=self.request.user, id=self.kwargs["datepoint_pk"]
            ).exists()
        else:
            return super(DatePointDetailView, self).test_func()


class DatePointUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    WorkerCanChangeDatePointDetail,
    UpdateView,
):

    model = DatePoint
    pk_url_kwarg = "datepoint_pk"

    fields = ["title", "task", "worked_time", "description", "url"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.approved_client:
            return HttpResponse(
                "Approved by client, cannot change", status=451
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.approved_manager = False
        return super(DatePointUpdateView, self).form_valid(form)

    permission_required = "projects.change_datepoint"


class DatePointListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    ListView,
):
    model = DatePoint

    context_object_name = "datepoints"

    def get_queryset(self):

        # Get new queryset
        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["project_pk"],
            worked_date=self.kwargs["date"],
        )

        return queryset

    def get_context_data(self, **kwargs):

        # Get context.
        context = super().get_context_data(**kwargs)

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["project_pk"],
            worked_date=self.kwargs["date"],
        )

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context

    permission_required = "projects.view_datepoint"


class ApproveDatePointView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    View,
):

    permission_required = "projects.change_datepoint"

    def get(self, *args, **kwargs):

        user = get_object_or_404(User, id=self.request.user.id)

        datepoint_pk = kwargs["datepoint_pk"]
        datepoint = get_object_or_404(DatePoint, id=datepoint_pk)

        if user.groups.count() > 0:
            if user.groups.all()[0].name == "Manager":
                datepoint.approved_manager = not datepoint.approved_manager
                datepoint.save()
                return HttpResponse(datepoint.approved_manager)
            elif user.groups.all()[0].name == "Client":
                datepoint.approved_client = not datepoint.approved_client
                datepoint.save()
                return HttpResponse(datepoint.approved_client)

        return HttpResponse(status=403)


class ManagerEndProjectPhase(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    View,
):

    permission_required = "projects.change_projectphase"

    def get(self, *args, **kwargs):

        user = self.request.user

        projectphase_pk = kwargs["projectphase_pk"]
        projectphase = get_object_or_404(ProjectPhase, id=projectphase_pk)

        if projectphase.ongoing is False:
            raise Http404("Cannot change phase to ongoing.")

        if user.groups.exists():
            if user.groups.all()[0].name == "Manager":
                projectphase.ongoing = False
                projectphase.save()
                return HttpResponse(f"{projectphase.title} has ended.")
        return HttpResponse(status=403)


class ManagerEndProject(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    View,
):

    permission_required = "projects.change_project"

    def get(self, *args, **kwargs):

        user = self.request.user

        project_pk = kwargs["project_pk"]
        project = get_object_or_404(Project, id=project_pk)

        if project.ongoing is False:
            raise Http404("Cannot change phase to ongoing.")

        if user.groups.count() > 0:
            if user.groups.all()[0].name == "Manager":
                for phase in project.projectphase_set.all():
                    phase.ongoing = False
                    phase.save()

                project.ongoing = False
                project.save()
                return HttpResponse(f"{project.title} has ended.")


# class WorkerDatePointListView(
#     LoginRequiredMixin,
#     PermissionRequiredMixin,
#     UserBelongsToProjectMixin,
#     ListView,
# ):
#     model = DatePoint

#     context_object_name = "datepoints"

#     ordering = ["-worked_date"]

#     def get_queryset(self):

#         worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

#         # Get new queryset
#         queryset = DatePoint.objects.filter(
#             task__project_id=self.kwargs["project_pk"], worker=worker
#         ).order_by("worked_date")

#         return queryset

#     def get_context_data(self, **kwargs):
#         # TODO: This functions is probably useless because ListView
#         # should already provide this data to the template.

#         # Get context.
#         context = super().get_context_data(**kwargs)

#         worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

#         queryset = DatePoint.objects.filter(
#             task__project_id=self.kwargs["project_pk"], worker=worker
#         ).order_by("worked_date")

#         datepoints_pks = [item.pk for item in queryset]

#         context["datepoints_pks"] = json.dumps(datepoints_pks)

#         return context

#     permission_required = "projects.view_datepoint"


def home(request):
    return render(request, "projects/home.html", context={"home_view": True})


# class ProjectPhaseBill(
#     LoginRequiredMixin,
#     PermissionRequiredMixin,
#     UserBelongsToProjectMixin,
#     PDFTemplateView,
# ):
#     permission_required = "projects.view_projectphase"
#     filename = "bill.pdf"
#     template_name = "projects/bill.html"

#     def test_func(self):
#         if self.request.user.groups.filter(
#             name="Manager"
#         ) or self.request.user.groups.filter(name="Client"):
#             return super(ProjectPhaseBill, self).test_func()
#         else:
#             return False

#     def get_context_data(self, **kwargs):
#         context = super(ProjectPhaseBill, self).get_context_data(**kwargs)

#         projectphase = get_object_or_404(
#             ProjectPhase, id=self.kwargs["projectphase_pk"]
#         )
#         price_per_hour = projectphase.project.price_per_hour

#         client_detail = {
#             "name": projectphase.project.client_detail.name,
#             "street": projectphase.project.client_detail.street,
#             "postal_code": projectphase.project.client_detail.postal_code,
#             "city": projectphase.project.client_detail.city,
#             "nip": projectphase.project.client_detail.nip,
#         }

#         context["client_detail"] = client_detail

#         if price_per_hour is None:
#             raise Http404(
#                 "Price is not set, please contact the administrator."
#             )

#         tasks = Task.objects.filter(project_id=self.kwargs["projectphase_pk"])

#         services = []
#         total_hours = 0

#         for task in tasks:
#             datepoints = DatePoint.objects.filter(task=task)

#             hours = 0
#             for datepoint in datepoints:
#                 if datepoint.approved_client and datepoint.approved_manager:
#                     hours += datepoint.worked_time
#                     total_hours += datepoint.worked_time

#             service = {
#                 "title": task.title,
#                 "count": hours,
#                 "price": f"{price_per_hour:.2f}".replace(".", ","),
#                 "brutto": f"{price_per_hour * hours:.2f}".replace(".", ","),
#                 "netto": f"{price_per_hour * hours:.2f}".replace(".", ","),
#             }

#             if hours != 0:
#                 services.append(service)

#         context["services"] = services

#         total = 0
#         total = total_hours * price_per_hour
#         context["total"] = f"{total:.2f}".replace(".", ",")
#         context["data"] = datetime.datetime.today()

#         return context


# class ProjectBill(
#     LoginRequiredMixin,
#     PermissionRequiredMixin,
#     UserBelongsToProjectMixin,
#     PDFTemplateView,
# ):
#     permission_required = "projects.view_projectphase"
#     filename = "bill.pdf"
#     template_name = "projects/bill.html"

#     def test_func(self):
#         if self.request.user.groups.filter(
#             name="Manager"
#         ) or self.request.user.groups.filter(name="Client"):
#             return super(ProjectBill, self).test_func()
#         else:
#             return False

#     def get_context_data(self, **kwargs):
#         context = super(ProjectBill, self).get_context_data(**kwargs)

#         project = get_object_or_404(Project, id=self.kwargs["project_pk"])
#         price_per_hour = project.price_per_hour

#         client_detail = {
#             "name": project.client_detail.name,
#             "street": project.client_detail.street,
#             "postal_code": project.client_detail.postal_code,
#             "city": project.client_detail.city,
#             "nip": project.client_detail.nip,
#         }

#         context["client_detail"] = client_detail

#         if price_per_hour is None:
#             raise Http404(
#                 "Price is not set, please contact the administrator."
#             )

#         projectphases = project.projectphase_set.all()

#         services = []
#         total_hours = 0

#         for projectphase in projectphases:
#             queryset = DatePoint.objects.filter(task__project=projectphase)

#             hours = 0

#             for datepoint in queryset:
#                 if datepoint.approved_client and datepoint.approved_manager:
#                     hours += datepoint.worked_time
#                     total_hours += datepoint.worked_time

#             service = {
#                 "title": projectphase.title,
#                 "count": hours,
#                 "price": f"{price_per_hour:.2f}".replace(".", ","),
#                 "brutto": f"{price_per_hour * hours:.2f}".replace(".", ","),
#                 "netto": f"{price_per_hour * hours:.2f}".replace(".", ","),
#             }

#             if hours != 0:
#                 services.append(service)

#         context["services"] = services

#         total = total_hours * price_per_hour
#         context["total"] = f"{total:.2f}".replace(".", ",")
#         context["data"] = datetime.datetime.today()

#         return context


class WorkerSummaryView(
    LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView
):
    model = User
    pk_url_kwarg = "worker_pk"
    form_class = WorkerMonthForm
    template_name = "projects/user_detail.html"

    def test_func(self):
        return self.request.user == User.objects.get(
            id=self.kwargs["worker_pk"]
        )

    def get_form_kwargs(self):
        kwargs = super(WorkerSummaryView, self).get_form_kwargs()

        worker = User.objects.get(id=self.kwargs["worker_pk"])

        kwargs["dates"] = worker.profile.get_dates()

        return kwargs

    def get_context_data(self, **kwargs):

        worker_summary_view = False

        context = super().get_context_data(**kwargs)

        try:
            self.kwargs["worker_summary_view"]
        except KeyError:
            pass
        else:
            worker = get_object_or_404(User, id=self.kwargs["worker_pk"])
            month = self.kwargs["month"]
            year = self.kwargs["year"]
            queryset = DatePoint.objects.filter(
                worker=worker, worked_date__month=month, worked_date__year=year
            ).order_by("-worked_date")
            worker_summary_view = True
            context["worker_summary_view"] = True

        if worker_summary_view:
            projects = Project.objects.filter(worker=worker)

            projects_dict = {}
            total_hours = 0

            for project in projects:
                projects_dict[f"{project.id}"] = 0

            for project in projects:
                for phase in project.projectphase_set.all():
                    queryset = DatePoint.objects.filter(
                        task__project=phase,
                        worker=worker,
                        worked_date__month=month,
                        worked_date__year=year,
                    )

                    for datepoint in queryset:
                        if datepoint.task.project.project.client.exists():
                            if (
                                datepoint.approved_manager
                                and datepoint.approved_client
                            ):
                                projects_dict[
                                    f"{datepoint.task.project.project.id}"
                                ] += datepoint.worked_time
                                total_hours += datepoint.worked_time
                        else:
                            if datepoint.approved_manager:
                                projects_dict[
                                    f"{datepoint.task.project.project.id}"
                                ] += datepoint.worked_time
                                total_hours += datepoint.worked_time

            services = []
            for project in projects:
                services.append(
                    {
                        "title": project.title,
                        "hours": projects_dict[f"{project.id}"],
                    }
                )

            if worker.profile.price_per_hour:
                context["total_hours"] = total_hours
                context["pay"] = total_hours * worker.profile.price_per_hour

            context["services"] = services

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            dates = form.cleaned_data["dates"]
            tmp_url = reverse(
                "worker-summary-month",
                kwargs={
                    "worker_pk": self.kwargs["worker_pk"],
                    "month": dates[5:7],
                    "year": dates[:4],
                },
            )
            return redirect(tmp_url)
