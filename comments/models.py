from django.db import models

from posts.models import TimeStampedModel, post


class comment(TimeStampedModel):
    comment = models.TextField()
    post_id = models.ForeignKey(post)
