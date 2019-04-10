from django.db import models
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    # Django will use this function to find a URL of any specific instance
    # of the Post.
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
