from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.title}, {self.description}, {self.user}'

    # Returns to project-detail page after creating the project.
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class Task(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    # Returns to project-detail page after creating task for the project.
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.pk})
