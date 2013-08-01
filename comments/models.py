# Relies on post model
from django.conf import settings
from django.db import models
from dbarray import IntegerArrayField

from posts.models import TimeStampedModel, post

COMMENT_SPAM_LIMIT = 2

class comment(TimeStampedModel):
    content = models.TextField()
    path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)
    post_id = models.ForeignKey(post, related_name='comments')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='comments')
    
    spam_count = models.SmallIntegerField(default=0)
    children = models.SmallIntegerField(default=0)
    up_votes = models.SmallIntegerField(default=0)
    total_votes = models.SmallIntegerField(default=0)
    vote_percentage = models.FloatField(default=0)

    def __unicode__(self):
        return self.content

    def update_votes(self, up_vote_to_add, total_vote_to_add):
        from votes.models import vote #Must import here b/c cross-relationship
        self.up_votes += up_vote_to_add
        self.total_votes += total_vote_to_add
        if self.total_votes != 0:
            self.vote_percentage = round(float(self.up_votes)/self.total_votes, 3)
        self.save()

    def check_spam_count(self):
        self.spam_count = self.spam_count + 1
        self.save()
        if self.spam_count >= COMMENT_SPAM_LIMIT:
            return True
        else:
            return False

