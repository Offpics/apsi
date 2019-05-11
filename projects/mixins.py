from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Project, Task


class UserBelongsToProjectMixin(UserPassesTestMixin):
    """ Check wheter user belongs to the Project. """

    def test_func(self):
        user = self.request.user
        project_pk = self.kwargs["pk"]
        if user.groups.all()[0].name == "Worker":
            queryset = Project.objects.filter(id=project_pk, worker=user)
            if queryset.count() > 0:
                return True
        elif user.groups.all()[0].name == "Manager":
            queryset = Project.objects.filter(id=project_pk, manager=user)
            if queryset.count() > 0:
                return True
        return False


class UserBelongsToTaskMixin(UserPassesTestMixin):
    """ Check wheter user belongs to the Task. """

    def test_func(self):
        user = self.request.user
        task_pk = self.kwargs["pk"]
        if user.groups.all()[0].name == "Worker":
            queryset = Task.objects.filter(id=task_pk, project__worker=user)
            if queryset.count() > 0:
                return True
        elif user.groups.all()[0].name == "Manager":
            queryset = Task.objects.filter(id=task_pk, project__worker=user)
            if queryset.count() > 0:
                return True
        return False
