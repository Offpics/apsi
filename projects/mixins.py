from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Project, Task, DatePoint


class UserBelongsToProjectMixin(UserPassesTestMixin):
    """ Check wheter user belongs to the Project. """

    def test_func(self):
        user = self.request.user
        project_pk = self.kwargs["project_pk"]
        return self.check_user(user, project_pk)

    def check_user(self, user, project_pk):
        if user.groups.count() > 0:
            if user.groups.all()[0].name == "Worker":
                queryset = Project.objects.filter(id=project_pk, worker=user)
                if queryset.count() > 0:
                    return True
            elif user.groups.all()[0].name == "Manager":
                queryset = Project.objects.filter(id=project_pk, manager=user)
                if queryset.count() > 0:
                    return True
        else:
            return False


class UserBelongsToTaskMixin(UserPassesTestMixin):
    """ Check wheter user belongs to the Task. """

    def test_func(self):
        user = self.request.user
        task_pk = self.kwargs["task_pk"]
        if user.groups.count() > 0:
            if user.groups.all()[0].name == "Worker":
                queryset = Task.objects.filter(
                    id=task_pk, project__worker=user
                )
                if queryset.count() > 0:
                    return True
            elif user.groups.all()[0].name == "Manager":
                queryset = Task.objects.filter(
                    id=task_pk, project__manager=user
                )
                if queryset.count() > 0:
                    return True
        else:
            return False


class ManagerCanEditDatepoint(UserPassesTestMixin):
    """ Check wheter user is manager and can edit a datepoint. """

    def test_func(self):
        user = self.request.user
        datepoint_pk = self.kwargs["datepoint_pk"]
        project_pk = DatePoint.objects.filter(id=datepoint_pk)[
            0
        ].task.project.id
        return self.check_user(user, project_pk)

    def check_user(self, user, project_pk):
        if user.groups.count() > 0:
            if user.groups.all()[0].name == "Manager":
                queryset = Project.objects.filter(id=project_pk, manager=user)
                if queryset.count() > 0:
                    return True
        else:
            return False


class UserCanViewDatePointDetail(
    UserBelongsToProjectMixin, UserPassesTestMixin
):
    """ Check wheter user can view the DatePoint.
    Get project id that datepoint relates to and
    checks wheter user belongs to this project id.
    """

    def test_func(self):
        datepoint_pk = self.kwargs["datepoint_pk"]
        project_pk = DatePoint.objects.filter(id=datepoint_pk)[
            0
        ].task.project.id

        user = self.request.user

        return super().check_user(user, project_pk)
