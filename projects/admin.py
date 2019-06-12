from django.contrib import admin
from django.contrib.auth.models import User

from .models import DatePoint, Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "description",
        "manager",
        "worker",
        "client",
        "price_per_hour",
    )
    list_display = ("title", "manager", "description")
    readonly_fields = ("title", "description", "worker")

    # filter_horizontal = ("worker", "client")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = User.objects.filter(groups__name="Manager")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "client":
            kwargs["queryset"] = User.objects.filter(groups__name="Client")

        if db_field.name == "worker":
            kwargs["queryset"] = User.objects.filter(groups__name="Worker")
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ("title", "project")
    readonly_fields = ("title",)
    list_display = ("title", "project")


@admin.register(DatePoint)
class DatePointAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "worker",
        "approved_manager",
        "worked_date",
        "worked_time",
        "date_created",
        "description",
        "url",
    )

    readonly_fields = (
        "task",
        "worker",
        "approved_manager",
        "worked_date",
        "worked_time",
        "date_created",
        "description",
        "url",
    )
