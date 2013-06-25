from django.contrib.auth.models import User
from django.db import models

class TimeStampedModel(models.Model):
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeModified = models.DateTimeField(auto_now=True)

    # Abstract base class
    class Meta:
        abstract = True


class Post(TimeStampedModel):
    # Leave this as 'name' b/c admin requires one
    name = models.CharField(default="", max_length=150)
    text = models.TextField()
    user_id = models.ForeignKey(User, related_name='posts')
                        # Allows us to access via user.posts

    # Better string representation in admin and elsewhere
    def __unicode__(self):
        return self.name
