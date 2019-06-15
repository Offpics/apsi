import json

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ClientDetail(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    nip = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    # Title of the project.
    title = models.CharField(max_length=100)

    # Description of the projet.
    description = models.TextField()

    # Manager of the project.
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="manager_project_set",
        null=True,
    )

    # Workers assigned to the project.
    worker = models.ManyToManyField(User, related_name="worker_project_set")

    # Client assigned to the project.
    client = models.ManyToManyField(User, related_name="client_project_set")

    # Price per hour.
    price_per_hour = models.PositiveIntegerField(blank=True, null=True)

    client_detail = models.ForeignKey(
        ClientDetail, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}, {self.manager}"

    # Returns to project-detail page after creating the project.
    def get_absolute_url(self):
        return reverse("project-list")


class ProjectPhase(models.Model):

    title = models.CharField(max_length=100, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    ongoing = models.BooleanField(default=True)

    # Dates in format [("m-Y", "m-Y"), ("m-Y", "m-Y")]
    dates = models.TextField(default="[]")

    first_datepoint = models.DateField(auto_now=True)
    last_datepoint = models.DateField(auto_now=True)

    def set_dates(self, dates):
        self.dates = json.dumps(dates)

    def get_dates(self):
        return json.loads(self.dates)

    def get_absolute_url(self):
        return reverse(
            "project-detail-temp", kwargs={"project_pk": self.project.id}
        )

    def __str__(self):
        return f"{self.title, self.project.title}"


class Task(models.Model):
    # Title of the task.
    title = models.CharField(max_length=100)

    # ForeignKey to Project.
    project = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE)

    # Description of the projet.
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.project.ongoing:
            raise ValueError(
                f"{self.project.title} has ended. Unable to insert new data."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    # Returns to project-detail page after creating task for the project.
    def get_absolute_url(self):
        return reverse(
            "projectphase-detail", kwargs={"projectphase_pk": self.project.id}
        )


class DatePoint(models.Model):
    # ForeignKey to Task.
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    # ForeignKey to Worker.
    worker = models.ForeignKey(User, on_delete=models.CASCADE)

    # Title of the datepoint.
    title = models.CharField(max_length=100)

    # Description of the working.
    description = models.CharField(max_length=100, blank=True)

    # URL to something.
    url = models.URLField(blank=True)

    # Worked time.
    worked_time = models.PositiveIntegerField()

    # Worked date.
    worked_date = models.DateField()

    # Time of the creation.
    date_created = models.DateTimeField(auto_now=True)

    # Wheter approved by manager.
    approved_manager = models.BooleanField(default=False)

    # Wheter approved by client.
    approved_client = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.task.project.ongoing:
            raise ValueError(
                f"{self.task.project.title} has ended. Unable to insert new data."
            )

        if type(self.worked_date) is str:
            projectphase = self.task.project
            dates = projectphase.get_dates()
            tmp = self.worked_date[:7]

            print(f"{dates}, {tmp}")

            tmp_in_dates = False
            for sublist in dates:
                if tmp in sublist:
                    tmp_in_dates = True
                    break

            if not tmp_in_dates:
                print("Appended")
                dates.append((tmp, tmp))
                projectphase.dates = json.dumps(dates)
                projectphase.save(update_fields=["dates"])

            print(dates)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Worker: {self.worker}, Task: {self.task}"

    # Returns to project-detail page after creating datepoint for the project.
    def get_absolute_url(self):
        return reverse(
            "worker-projectphase-detail",
            kwargs={"projectphase_pk": self.task.project.pk},
        )
