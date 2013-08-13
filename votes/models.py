# Relies on post, comment model
from django.conf import settings
from django.db import models
from model_utils import Choices
from posts.models import post
from comments.models import comment


class vote(models.Model):

    VOTE_CHOICES = Choices(
        ('upvote'),
        ('downvote'),
    )

    post_id = models.ForeignKey(post, related_name='votes', null=True)
    comment_id = models.ForeignKey(comment, related_name='votes', null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
    vote_choice = models.CharField(max_length=8, choices=VOTE_CHOICES,
                                   default=VOTE_CHOICES.upvote)


# Purpose - To limit users to one "Mark as spam" vote
class spam(models.Model):
    post_id = models.ForeignKey(post, related_name='spam', null=True)
    comment_id = models.ForeignKey(comment, related_name='spam', null=True)

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='spam')
