from django.db import models
from dbarray import IntegerArrayField

from posts.models import TimeStampedModel

 
class comment(TimeStampedModel):
    content = models.TextField()
    path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.content

"""
from django.conf import settings

class comment(TimeStampedModel):
    comment = models.TextField()
    post_id = models.ForeignKey(post, related_name='comments')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='comments')
"""
