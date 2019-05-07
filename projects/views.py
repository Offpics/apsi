from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from .models import Project, Task


class ProjectCreateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        SuccessMessageMixin,
                        CreateView):
    model = Project
    fields = ['title', 'description', 'user']
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

    fields = ['title', 'description', 'user']

    permission_required = 'projects.update_project'


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
