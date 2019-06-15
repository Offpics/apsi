from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Project, Task, DatePoint, ProjectPhase


class UserBelongsToProjectMixin(UserPassesTestMixin):
    """ Check wheter user belongs to the Project. """

    def test_func(self):
        user = self.request.user
        try:
            project_pk = self.kwargs["project_pk"]
        except KeyError:
            pass
        else:
            return self.check_user_project(user, project_pk)

        try:
            projectphase_pk = self.kwargs["projectphase_pk"]
        except KeyError:
            pass
        else:
            return self.check_user_projectphase(user, projectphase_pk)

        try:
            datepoint_pk = self.kwargs["datepoint_pk"]
        except KeyError:
            pass
        else:
            return self.check_user_datepoint(user, datepoint_pk)

        return False

    def check_user_datepoint(self, user, datepoint_pk):
        if user.groups.exists():
            if user.groups.all()[0].name == "Worker":
                queryset = DatePoint.objects.filter(
                    id=datepoint_pk, task__project__project__worker=user
                )
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Manager":
                queryset = DatePoint.objects.filter(
                    id=datepoint_pk, task__project__project__manager=user
                )
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Client":
                queryset = DatePoint.objects.filter(
                    id=datepoint_pk, task__project__project__client=user
                )
                if queryset.exists():
                    return True
        else:
            return False

    def check_user_projectphase(self, user, projectphase_pk):
        if user.groups.exists():
            if user.groups.all()[0].name == "Worker":
                queryset = ProjectPhase.objects.filter(
                    id=projectphase_pk, project__worker=user
                )
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Manager":
                queryset = ProjectPhase.objects.filter(
                    id=projectphase_pk, project__manager=user
                )
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Client":
                queryset = ProjectPhase.objects.filter(
                    id=projectphase_pk, project__client=user
                )
                if queryset.exists():
                    return True
        else:
            return False

    def check_user_project(self, user, project_pk):
        if user.groups.exists():
            if user.groups.all()[0].name == "Worker":
                queryset = Project.objects.filter(id=project_pk, worker=user)
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Manager":
                queryset = Project.objects.filter(id=project_pk, manager=user)
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Client":
                queryset = Project.objects.filter(id=project_pk, client=user)
                if queryset.exists():
                    return True
        else:
            return False


class UserBelongsToTaskMixin(UserPassesTestMixin):
    """ Check wheter user belongs to the Task. """

    def test_func(self):
        user = self.request.user
        task_pk = self.kwargs["task_pk"]
        if user.groups.exists():
            if user.groups.all()[0].name == "Worker":
                queryset = Task.objects.filter(
                    id=task_pk, project__project__worker=user
                )
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Manager":
                queryset = Task.objects.filter(
                    id=task_pk, project__project__manager=user
                )
                if queryset.exists():
                    return True
            elif user.groups.all()[0].name == "Client":
                queryset = Task.objects.filter(
                    id=task_pk, project__project__client=user
                )
                if queryset.exists():
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
        return self.check_user_project(user, project_pk)

    def check_user_project(self, user, project_pk):
        if user.groups.exists():
            if user.groups.all()[0].name == "Manager":
                queryset = Project.objects.filter(id=project_pk, manager=user)
                if queryset.exists():
                    return True
            if user.groups.all()[0].name == "Client":
                queryset = Project.objects.filter(id=project_pk, client=user)
                if queryset.exists():
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

        return super().check_user_project(user, project_pk)


class WorkerCanChangeDatePointDetail(UserPassesTestMixin):
    def test_func(self):
        datepoint_pk = self.kwargs["datepoint_pk"]
        user = self.request.user

        return DatePoint.objects.filter(id=datepoint_pk, worker=user).exists()
