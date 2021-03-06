from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.fields import DateTimeField
from django.urls import reverse

from bumblebee.users.models import CustomUser

######################################
#           BUZZ
######################################


class AbstractBuzz(models.Model):
    """
    A post for Content
    """

    class PrivacyChoices(models.TextChoices):
        """
        Choices for privacy options
        """

        PRIVATE = "priv", "private"  # only for self
        PUBLIC = "pub", "public"  # open for anyone public
        PROTECTED = "prot", "protected"  # only for followers

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    # self
    privacy = models.CharField(
        max_length=25, choices=PrivacyChoices.choices, default=PrivacyChoices.PUBLIC
    )
    content = models.CharField(
        max_length=1000,
        help_text="Something in your mind? Post a buzz",
        blank=True,
        null=True,
    )

    location = models.CharField(max_length=500, blank=True, null=True)
    flair = ArrayField(models.CharField(max_length=100), blank=True, default=list)

    sentiment_value = models.FloatField(null=True, blank=True)
    textblob_value = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_privacy_options(self):
        return self.PrivacyChoices.choices


class Buzz(AbstractBuzz):
    """ """

    author = models.ForeignKey(
        CustomUser, related_name="author_buzz", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Buzz"
        verbose_name_plural = "Buzzes"
        ordering = ["-created_date"]

    def __str__(self):
        """ """
        return f"id:{self.id} content:`{self.content}`"

    def get_absolute_url(self):
        """ """
        return reverse("buzz-detail", kwargs={"buzzid": self.id})


class Rebuzz(AbstractBuzz):
    """
    Rebuzz post of a buzz
    """

    # referenced buzz
    buzz = models.ForeignKey(
        Buzz,
        related_name="buzz_rebuzz",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )

    author = models.ForeignKey(
        CustomUser, related_name="author_rebuzz", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Rebuzz"
        verbose_name_plural = "Rebuzzes"

    def __str__(self):
        """ """
        return f"id:{self.id} content:`{self.content}`"

    def get_absolute_url(self):
        """ """
        return reverse("rebuzz-detail", kwargs={"rebuzzid": self.id})

    def get_privacy_options(self):
        return self.PrivacyChoices.choices

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("rebuzz-detail", kwargs={"id": self.id})


######################################
#           BUZZ INTERACTIONS
######################################


class AbstractBuzzInteractions(models.Model):
    """ """

    updated_date = models.DateTimeField(auto_now=True)

    upvotes = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    downvotes = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    comments = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    rebuzzes = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"Interactions for Buzz: id-{self.buzz.id}"

    def get_upvote_count(self):
        return len(self.upvotes)

    def get_downvote_count(self):
        return len(self.downvotes)

    def get_comment_count(self):
        return len(self.comments)

    def get_rebuzz_count(self):
        return len(self.rebuzzes)


class BuzzInteractions(AbstractBuzzInteractions):
    """ """

    buzz = models.OneToOneField(
        Buzz,
        related_name="buzz_interaction",
        on_delete=models.CASCADE,
    )


class RebuzzInteractions(AbstractBuzzInteractions):
    """ """

    rebuzz = models.OneToOneField(
        Rebuzz,
        name="rebuzz",
        related_name="rebuzz_interaction",
        on_delete=models.CASCADE,
    )


######################################
#           BUZZ UPVDWV META
######################################


class UpvoteDownvoteMetaAbstract(models.Model):
    """ """

    class ActionChoices(models.TextChoices):
        """
        Choices for action options
        """

        UPVOTE = "upv", "upvote"
        PUBLIC = "downvote", "downvote"  # open for anyone public

    action = models.CharField(max_length=100, choices=ActionChoices.choices)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BuzzUpvoteDownvoteMeta(UpvoteDownvoteMetaAbstract):
    """ """

    agent = models.ForeignKey(
        CustomUser, related_name="user_buzz_upvdwv_meta", on_delete=models.CASCADE
    )

    buzz_interaction = models.ForeignKey(
        BuzzInteractions,
        related_name="buzz_interaction_upvdwv_meta",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"userid: {self.userid} {self.action} Buzz on {self.date}"


class RebuzzUpvoteDownvoteMeta(UpvoteDownvoteMetaAbstract):
    """ """

    agent = models.ForeignKey(
        CustomUser, related_name="user_rebuzz_upvdwv_meta", on_delete=models.CASCADE
    )

    rebuzz_interaction = models.ForeignKey(
        RebuzzInteractions,
        related_name="rebuzz_interaction_upvdwv_meta",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"userid: {self.userid} {self.action} Rebuzz on {self.date}"


######################################
#           BUZZ IMAGES
######################################


class AbstractBuzzImage(models.Model):
    """ """

    image = models.ImageField(
        upload_to="buzzes/image",
        help_text="Select Images. Maximum 8 allowed",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        """ """

        return self.image.path


class BuzzImage(AbstractBuzzImage):
    """ """

    buzz = models.ForeignKey(
        Buzz,
        related_name="buzz_image",
        on_delete=models.CASCADE,
    )


class RebuzzImage(AbstractBuzzImage):
    """ """

    rebuzz = models.OneToOneField(
        Rebuzz,
        name="rebuzz",
        related_name="rebuzz_image",
        on_delete=models.CASCADE,
    )
