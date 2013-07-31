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


    def __unicode__(self):
        return self.content

    def check_spam_count(self):
        self.spam_count = self.spam_count + 1
        self.save()
        if self.spam_count >= COMMENT_SPAM_LIMIT:
            return True
        else:
            return False

# Purpose - To limit users to one "Mark as spam" vote
class spam(models.Model):
    post_id = models.ForeignKey(post, related_name='spam', null=True)
    comment_id = models.ForeignKey(comment, related_name='spam', null=True)

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='spam')

