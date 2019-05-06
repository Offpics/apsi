from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.title}, {self.description}, {self.user}'

    # Django will use this function to find a URL of any specific instance
    # of the Post.
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
