from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

USER_TYPE_CHOICES = (
    ('AD', "Admin"),
    ('CL', "Clinician")
)
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=500, blank=True)
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default='CL')
    # If we want to add more fields add them here!
    # Then go to accounts/views.py

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
