from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from bumblebee.activities.models import UserActivity
from bumblebee.activities.utils import _create_activity
from bumblebee.connections.models import Blocked, Follower, Following, Muted
from bumblebee.profiles.models import Profile
from config.definitions import DEBUG

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def post_save_create_save_profile_and_activity(sender, instance, created, **kwargs):
    if created:
        if DEBUG:
            print(
                f"`post_save_create_save_profile_and_activity` signal received!",
            )

        # create profile
        profile = Profile.objects.create(user=instance)
        follower = Follower.objects.create(user=instance)
        following = Following.objects.create(user=instance)
        muted = Muted.objects.create(user=instance)
        blocked = Blocked.objects.create(user=instance)

        _create_activity(
            user=instance,
            action=UserActivity.Actions.SIGN_UP,
            target_content=ContentType.objects.get_for_model(CustomUser),
            target_id=instance.id,
        )
        # profile
        _create_activity(
            user=instance,
            action=UserActivity.Actions.CREATE,
            target_content=ContentType.objects.get_for_model(Profile),
            target_id=profile.id,
        )


# TODO custom email verified signal
