from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from .models import Project, Task
from .forms import ProjectCreateForm


class ProjectCreateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        SuccessMessageMixin,
                        CreateView):

    form_class = ProjectCreateForm
    template_name = "projects/project_form.html"

    def form_valid(self, form):
        # Get project by id.
        manager = get_object_or_404(User, id=self.request.user.id)

        # Append the form with returned project.
        form.instance.manager = manager

        # Create new Task.
        return super(ProjectCreateView, self).form_valid(form)

    success_message = 'Project succesfully created!'

    permission_required = 'projects.add_project'


class ProjectDetailView(PermissionRequiredMixin, DetailView):
    model = Project

    permission_required = 'projects.view_project'


class ProjectListView(PermissionRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'

    permission_required = 'projects.view_project'


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project

    form_class = ProjectCreateForm
    template_name = "projects/project_form.html"

    permission_required = 'projects.change_project'


class MyProjectsListView(LoginRequiredMixin, ListView):
    """ Returns ListView with projects that authenticated user belongs to. """
    template_name = 'projects/project_list'
    context_object_name = 'projects'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = Project.objects.filter(manager=user)
        if (len(queryset) == 0):
            queryset = Project.objects.filter(worker=user)
        return queryset


class TaskCreateView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    fields = ['title']

    # This function is called when valid form data has been Posted.
    # It gets current project id from url and attach it to the new Task
    # and saving it.
    def form_valid(self, form):
        # Get project by id.
        project = get_object_or_404(Project, id=self.kwargs['pk'])

        # Append the form with returned project.
        form.instance.project = project

        # Create new Task.
        return super(TaskCreateView, self).form_valid(form)

    success_message = 'Task succesfully created!'

    permission_required = 'projects.add_task'


def home(request):
    return render(request, 'projects/home.html')
