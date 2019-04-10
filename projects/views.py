from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .models import Project


class ProjectCreateView(CreateView):
    model = Project
    fields = ['title', 'description']


class ProjectDetailView(DetailView):
    model = Project


def home(request):
    return render(request, 'projects/home.html')
