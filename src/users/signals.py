from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_profiles.models import UserProfile


# post_save is the signal we want to listen to.
# sender is the model that triggers the signal
# when it gets saved.
# @received decorator marks this function as a
# listener to the provided signal.
#
# It's recommended to keep signal definitions
# in apps which models are triggering signal
# broadcasting. Each app can define its own
# listeners for the same signal. These listeners
# will be executed separately.
#
# We can also create our own signals:
# from django.dispatch import Signal
# user_verified = Signal()
#
# from your_app.signals import user_verified
# user_verified.send(user=request.user)
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
