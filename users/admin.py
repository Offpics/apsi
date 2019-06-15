from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib import admin
from .models import Profile


UserAdmin.add_fieldsets = (
    (None, {"fields": ("username", "password1", "password2", "groups")}),
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ("user", "price_per_hour")
    list_display = ("user", "price_per_hour")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
