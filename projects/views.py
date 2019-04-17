from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Project


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


def home(request):
    return render(request, 'projects/home.html')
