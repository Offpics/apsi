from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib import admin


UserAdmin.add_fieldsets = (
    (None, {"fields": ("username", "password1", "password2", "groups")}),
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
