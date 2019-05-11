from django.contrib import admin

from .models import DatePoint, Project, Task

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(DatePoint)
