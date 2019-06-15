from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        if not instance.groups.filter(name="Worker").exists():
            instance.profile.save()
