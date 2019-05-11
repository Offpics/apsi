from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import DatePointCreateForm, ProjectCreateForm
from .mixins import UserBelongsToProjectMixin, UserBelongsToTaskMixin
from .models import DatePoint, Project, Task


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
    PermissionRequiredMixin, UserBelongsToProjectMixin, DetailView
):
    model = Project

    permission_required = "projects.view_project"


class ProjectListView(PermissionRequiredMixin, ListView):
    model = Project
    context_object_name = "projects"

    permission_required = "projects.view_project"


class ProjectUpdateView(
    PermissionRequiredMixin,
    UserBelongsToProjectMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Project

    form_class = ProjectCreateForm
    template_name = "projects/project_form.html"

    success_message = "Project succesfully updated!"

    permission_required = "projects.change_project"


class MyProjectsListView(LoginRequiredMixin, ListView):
    """ Returns ListView with projects that authenticated user belongs to. """

    template_name = "projects/project_list"
    context_object_name = "projects"

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = Project.objects.filter(manager=user)
        if len(queryset) == 0:
            queryset = Project.objects.filter(worker=user)
        return queryset


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
        project = get_object_or_404(Project, id=self.kwargs["pk"])

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the datepoints.
        datepoint_list = DatePoint.objects.filter(task__id=self.kwargs["pk"])
        context["datepoint_list"] = datepoint_list
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

    success_message = "Task succesfully updated!"

    permission_required = "projects.change_task"


class DatePointCreateView(
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = DatePointCreateForm
    template_name = "projects/datepoint_form.html"

    def get_form_kwargs(self):
        kwargs = super(DatePointCreateView, self).get_form_kwargs()

        # Add current user to the form.
        kwargs["user"] = self.request.user

        # Add curent project id to the form.
        kwargs["pk"] = self.kwargs["pk"]

        return kwargs

    def form_valid(self, form):
        worker = get_object_or_404(User, id=self.request.user.id)

        form.instance.worker = worker

        return super(DatePointCreateView, self).form_valid(form)

    success_message = "DatePoint succesfully created!"

    permission_required = "projects.add_datepoint"


def home(request):
    return render(request, "projects/home.html")
