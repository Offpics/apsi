from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Project, Task


def does_user_belongs_to_project(user_id, project_pk):
    """ Check wheter user belongs to the project. """
    user = get_object_or_404(User, id=user_id)
    if user.groups.all()[0].name == 'Worker':
        queryset = Project.objects.filter(id=project_pk, worker=user)
        if queryset.count() > 0:
            return True
    elif user.groups.all()[0].name == 'Manager':
        queryset = Project.objects.filter(id=project_pk, manager=user)
        if queryset.count() > 0:
            return True
    return False


def does_user_belongs_to_task(user_id, task_pk):
    """ Check wheter user belongs to the task. """
    user = get_object_or_404(User, id=user_id)
    if user.groups.all()[0].name == 'Worker':
        queryset = Task.objects.filter(id=task_pk, project__worker=user)
        if queryset.count() > 0:
            return True
    elif user.groups.all()[0].name == 'Manager':
        queryset = Task.objects.filter(id=task_pk, project__manager=user)
        if queryset.count() > 0:
            return True
    return False
