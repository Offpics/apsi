from django.contrib import admin
from django.contrib.auth.models import User

from .models import DatePoint, Project, Task, ClientDetail, ProjectPhase


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "description",
        "manager",
        "worker",
        "client",
        "price_per_hour",
        "client_detail",
        "ongoing",
    )
    list_display = (
        "title",
        "ongoing",
        "manager",
        "client_detail",
        "description",
    )
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


@admin.register(ProjectPhase)
class ProjectPhase(admin.ModelAdmin):
    readonly_fields = ("first_datepoint", "last_datepoint", "dates")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ("title", "description", "project")
    readonly_fields = ("title", "description")
    list_display = ("title", "project", "description")


@admin.register(DatePoint)
class DatePointAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "worker",
        "approved_manager",
        "approved_client",
        "worked_date",
        "worked_time",
        "title",
        "description",
        "url",
    )

    readonly_fields = (
        "task",
        "worker",
        "approved_manager",
        "approved_client",
        "worked_date",
        "worked_time",
        "title",
        "description",
        "url",
    )


@admin.register(ClientDetail)
class ClientDetail(admin.ModelAdmin):
    list_display = ("name", "street", "postal_code", "city", "nip")
