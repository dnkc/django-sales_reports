# signals = communication system between django applications
# one app sends a signal, receiver performs an action

# here, receiver is profile app. will get made once a user is created

from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # created can be set to true only once - only when instance is created by sender
    if created:
        Profile.objects.create(user=instance)
