from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Project


class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = ['title', 'description', 'user']
    success_message = 'Project succesfully created!' 


class ProjectDetailView(DetailView):
    model = Project


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'

def home(request):
    return render(request, 'projects/home.html')
