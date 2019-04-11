from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'description']


class ProjectDetailView(DetailView):
    model = Project


def home(request):
    return render(request, 'projects/home.html')
