from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    # Title of the project.
    title = models.CharField(max_length=100)

    # Description of the projet.
    description = models.TextField()

    # Manager of the project.
    manager = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="manager_project_set")

    # Workers assigned to the project.
    worker = models.ManyToManyField(User, related_name="worker_project_set")

    def __str__(self):
        return f'{self.title}, {self.description}, {self.worker}'

    # Returns to project-detail page after creating the project.
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class Task(models.Model):
    # Title of the task.
    title = models.CharField(max_length=100)

    # ForeignKey to Project.
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    # Returns to project-detail page after creating task for the project.
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.pk})


class DatePoint(models.Model):
    # ForeignKey to Task.
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    # ForeignKey to Worker.
    worker = models.ForeignKey(User, on_delete=models.CASCADE)

    # Description of the working.
    description = models.CharField(max_length=100)
