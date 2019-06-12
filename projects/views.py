import json

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
    View,
)
from django.views.generic.edit import FormMixin

from .forms import (
    DatePointCreateForm,
    DatePointCreateForm2,
    ProjectCreateForm,
    QueryDatepointsForm,
)
from .mixins import (
    ManagerCanEditDatepoint,
    UserBelongsToProjectMixin,
    UserBelongsToTaskMixin,
    UserCanViewDatePointDetail,
)
from .models import DatePoint, Project, Task
from .utils import colors

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


class ProjectDetailView(
    PermissionRequiredMixin, FormMixin, UserBelongsToProjectMixin, DetailView
):
    """
    TODO: Change this View according to
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview.
    """

    model = Project
    form_class = QueryDatepointsForm
    pk_url_kwarg = "project_pk"

    def get_context_data(self, **kwargs):
        """ Populate context with DatePointCreateForm. """

        calendar_view = False
        table_view = False

        # Get context.
        context = super().get_context_data(**kwargs)

        # Get DatePoints that belong to current project.
        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["project_pk"]
        )

        try:
            self.kwargs["calendar_view"]
        except KeyError:
            pass
        else:
            calendar_view = True
            context["calendar_view"] = True

        try:
            self.kwargs["table_view"]
        except KeyError:
            pass
        else:
            table_view = True
            context["table_view"] = True

        try:
            worker = get_object_or_404(User, id=self.kwargs["worker_pk"])
        except KeyError:
            pass
        else:
            queryset = DatePoint.objects.filter(
                task__project_id=self.kwargs["project_pk"], worker=worker
            ).order_by("-worked_date")
            context["worker_name"] = worker.username

        try:
            task = get_object_or_404(Task, id=self.kwargs["task_pk"])
        except KeyError:
            pass
        else:
            queryset = DatePoint.objects.filter(task=task).order_by(
                "-worked_date"
            )

        try:
            self.kwargs["all"]
        except KeyError:
            pass
        else:
            queryset = DatePoint.objects.filter(
                task__project_id=self.kwargs["project_pk"]
            ).order_by("-worked_date")

        try:
            month = self.kwargs["month"]
            year = self.kwargs["year"]
        except KeyError:
            pass
        else:
            queryset = DatePoint.objects.filter(
                task__project_id=self.kwargs["project_pk"],
                worked_date__month=month,
                worked_date__year=year,
            ).order_by("-worked_date")

        if calendar_view:
            # Assign one color to one task and create dict of it.
            # tasks_color = dict(zip(tasks, colors))
            print("------")
            print(self.request.user.groups.all().exists)
            print("------")

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
                            "color": "green"
                            if item.approved_manager
                            else "red",
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
                            "color": "green"
                            if item.approved_client
                            else "red",
                        }
                        for item in queryset
                    ]

            # Create json and add it to context.
            context["datepoints"] = json.dumps(datepoints)
        elif table_view:

            context["datepoint_list"] = queryset

            datepoints_pks = [item.pk for item in queryset]

            context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            month = form.cleaned_data["month"]
            project_pk = kwargs["project_pk"]
            tmp_url = reverse(
                "project-date-table",
                kwargs={
                    "project_pk": project_pk,
                    "month": month,
                    "year": 2019,
                },
            )
            print(tmp_url)
            return redirect(tmp_url)
            # return redirect(f"{month}/2019/")

        # if form.is_valid():
        # print("VALID")
        # return self.form_valid(form)
        # else:
        # print("INVALID")
        # return self.form_invalid(form)

    # def form_valid(self, form):
    #     worker = get_object_or_404(User, id=self.request.user.id)

    #     form.instance.worker = worker

    #     form.save()
    #     messages.success(self.request, "Datepoint succesfully created!")

    #     return super(ProjectDetailView, self).form_valid(form)

    permission_required = "projects.view_project"


class ProjectUpdateView(
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

        # TODO: Refactor code below because this is not a proper check.
        queryset = Project.objects.filter(manager=user)
        if len(queryset) == 0:
            queryset = Project.objects.filter(worker=user)
        if len(queryset) == 0:
            queryset = Project.objects.filter(client=user)
        return queryset

    permission_required = "projects.view_project"


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
    SuccessMessageMixin,
    CreateView,
):
    model = Task
    fields = ["title"]

    # This function is called when valid form data has been Posted.
    # It gets current project id from url and attach it to the new Task
    # and saving it.
    def form_valid(self, form):
        # Get project by id.
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        # Append the form with returned project.
        form.instance.project = project

        # Create new Task.
        return super(TaskCreateView, self).form_valid(form)

    success_message = "Task succesfully created!"

    permission_required = "projects.add_task"


class TaskDetailView(
    PermissionRequiredMixin, UserBelongsToTaskMixin, DetailView
):
    model = Task
    pk_url_kwarg = "task_pk"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the datepoints.
        datepoint_list = DatePoint.objects.filter(
            task__id=self.kwargs["task_pk"]
        )
        context["datepoint_list"] = datepoint_list

        datepoints_pks = [item.pk for item in datepoint_list]

        context["datepoints_pks"] = datepoints_pks

        return context

    permission_required = "projects.view_task"


class TaskUpdateView(
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
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = DatePointCreateForm2
    template_name = "projects/datepoint_form.html"
    pk_url_kwarg = "project_pk"

    def get_form_kwargs(self):
        kwargs = super(DatePointCreateView, self).get_form_kwargs()

        # Add current user to the form.
        kwargs["user"] = self.request.user

        # Add curent project id to the form.
        kwargs["project_pk"] = self.kwargs["project_pk"]

        return kwargs

    def form_valid(self, form):
        form.instance.worker = self.request.user

        form.instance.worked_date = self.kwargs["date"]

        return super(DatePointCreateView, self).form_valid(form)

    success_message = "DatePoint succesfully created!"

    permission_required = "projects.add_datepoint"


class DatePointCreateView2(
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = DatePointCreateForm2
    template_name = "projects/datepoint_form.html"
    pk_url_kwarg = "task_pk"

    def get_form_kwargs(self):
        kwargs = super(DatePointCreateView, self).get_form_kwargs()

        # Add current user to the form.
        kwargs["user"] = self.request.user

        # Add curent project id to the form.
        kwargs["task_pk"] = self.kwargs["task_pk"]

        return kwargs

    def form_valid(self, form):
        task = get_object_or_404(Task, id=self.kwargs["task_pk"])
        form.instance.task = task

        form.instance.worker = self.request.user

        return super(DatePointCreateView, self).form_valid(form)

    success_message = "DatePoint succesfully created!"

    permission_required = "projects.add_datepoint"


class DatePointDetailView(
    PermissionRequiredMixin, UserCanViewDatePointDetail, DetailView
):
    model = DatePoint
    pk_url_kwarg = "datepoint_pk"

    permission_required = "projects.view_datepoint"


class DatePointListView(
    PermissionRequiredMixin, UserBelongsToProjectMixin, ListView
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


class ManagerApproveDatePointView(
    PermissionRequiredMixin, ManagerCanEditDatepoint, View
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


def home(request):
    return render(request, "projects/home.html")


class WorkerProjectDetailView(DetailView):
    model = Project
    form_class = DatePointCreateForm
    pk_url_kwarg = "project_pk"

    def get_context_data(self, **kwargs):
        """ Populate fullcalendar with datepoints. """

        # Get context.
        context = super().get_context_data(**kwargs)

        # Get DatePoints that belong to current worker.
        queryset = DatePoint.objects.filter(
            worker=self.request.user.id,
            task__project_id=self.kwargs["project_pk"],
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


class ManagerProjectDetailView(DetailView):

    model = Project
    form_class = DatePointCreateForm
    pk_url_kwarg = "project_pk"


class WorkerDatePointListView(
    PermissionRequiredMixin, UserBelongsToProjectMixin, ListView
):
    model = DatePoint

    context_object_name = "datepoints"

    ordering = ["-worked_date"]

    def get_queryset(self):

        worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

        # Get new queryset
        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["project_pk"], worker=worker
        ).order_by("worked_date")

        return queryset

    def get_context_data(self, **kwargs):
        # TODO: This functions is probably useless because ListView
        # should already provide this data to the template.

        # Get context.
        context = super().get_context_data(**kwargs)

        worker = get_object_or_404(User, id=self.kwargs["worker_pk"])

        queryset = DatePoint.objects.filter(
            task__project_id=self.kwargs["project_pk"], worker=worker
        ).order_by("worked_date")

        datepoints_pks = [item.pk for item in queryset]

        context["datepoints_pks"] = json.dumps(datepoints_pks)

        return context

    permission_required = "projects.view_datepoint"
