from django.contrib import admin

from .models import DatePoint, Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
    # list_display = ("title", "manager", "description", "client")

    # readonly_fields = ("worker",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project")


@admin.register(DatePoint)
class DatePointAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "worker",
        "approved",
        "worked_date",
        "worked_time",
        "date_created",
        "description",
        "url",
    )

    readonly_fields = (
        "task",
        "worker",
        "approved",
        "worked_date",
        "worked_time",
        "date_created",
        "description",
        "url",
    )
