from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices
from posts.models import post


class vote(models.Model):

    VOTE_CHOICES = Choices(
        ('upvote'),
        ('downvote'),
    )

    post_id = models.ForeignKey(post, related_name='votes')
    user_id = models.ForeignKey(get_user_model(), related_name='votes')
    vote_choice = models.CharField(max_length=8, choices=VOTE_CHOICES,
                                   default=VOTE_CHOICES.upvote)
