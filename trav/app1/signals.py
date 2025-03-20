from django.db.models.signals import post_save  # Signal that runs after saving a model instance
from django.contrib.auth.models import User  # Django's built-in User model
from django.dispatch import receiver  # Used to connect signals
from .models import Profile  # Import the Profile model

@receiver(post_save, sender=User)  # Runs after a User object is saved
def create_profile(sender, instance, created, **kwargs):
    if created:  # Check if a new User was created
        Profile.objects.create(user=instance)  # Create a Profile linked to the User

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # Save the Profile when User is saved
