from django.conf import settings
from django.db import models

from posts.models import TimeStampedModel, post


class comment(TimeStampedModel):
    comment = models.TextField()
    post_id = models.ForeignKey(post, related_name="comments")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
