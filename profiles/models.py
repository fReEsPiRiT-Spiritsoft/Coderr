"""Profile model and user signals.

Defines the `Profile` model which is created automatically when a new
`User` is created. The module registers two signal handlers: one to
create the profile on user creation and another to save the profile
when the user is saved.
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Additional information attached to a Django `User`.

    Fields include a `type` (customer/business), optional image/file
    and contact/location metadata.
    """

    PROFILE_TYPE_CHOICES = (("customer", "customer"), ("business", "business"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, default="customer")
    description = models.TextField(blank=True, default="")
    file = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a `Profile` with default values when a new `User` is created."""

    if created:
        Profile.objects.create(user=instance, type="customer")


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Ensure the related `Profile` is saved when the `User` is saved."""

    if hasattr(instance, "profile"):
        instance.profile.save()