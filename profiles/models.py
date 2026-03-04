from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('customer', 'customer'),
        ('business', 'business'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, default='customer')
    description = models.TextField(blank=True, default='')
    file = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=50, blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.type}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, type='customer')


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()