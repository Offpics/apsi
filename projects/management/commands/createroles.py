from projects.models import Project

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


THINGS = [
    {
        "group_name": "Manager",
        "models": [
            {"name": "project", "permissions": ["view", "change", "add"]},
            {"name": "task", "permissions": ["add", "change", "view"]},
            {"name": "date point", "permissions": ["change", "view"]},
        ],
    },
    {
        "group_name": "Worker",
        "models": [
            {"name": "project", "permissions": ["view"]},
            {"name": "task", "permissions": ["view"]},
            {"name": "date point", "permissions": ["view", "add", "change"]},
        ],
    },
    {
        "group_name": "Client",
        "models": [
            {"name": "project", "permissions": ["view"]},
            {"name": "task", "permissions": ["view"]},
            {"name": "date point", "permissions": ["view", "change"]},
        ],
    },
    {
        "group_name": "Smrodek5",
        "models": [
            {"name": "project", "permissions": ["view"]},
            {"name": "task", "permissions": ["view"]},
            {"name": "date point", "permissions": ["view", "change", "add"]},
        ],
    },
]


class Command(BaseCommand):
    help = "Creates roles necessary to work with app."

    def handle(self, *args, **options):
        for item in THINGS:
            new_group, created = Group.objects.get_or_create(
                name=item["group_name"]
            )
            print(f"---------------{item['group_name']}----------------")
            for model in item["models"]:
                for permission in model["permissions"]:
                    name = f"Can {permission} {model['name']}"
                    print(f"Creating {name}")

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        print("Model does not exists in database!")
                        print("You have to make migrations!")
                        raise
                    else:
                        new_group.permissions.add(model_add_perm)

            print("Created all groups and permissions :)")

