from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'description', 'user']


class ProjectDetailView(DetailView):
    model = Project


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'

def home(request):
    return render(request, 'projects/home.html')
