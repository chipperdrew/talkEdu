from django.db import models

class TimeStampedModel(models.Model):
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeModified = models.DateTimeField(auto_now=True)

    # Abstract base class
    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(default="", max_length=75)
    text = models.TextField()

    # Better string representation in admin and elsewhere
    def __unicode__(self):
        return self.name
