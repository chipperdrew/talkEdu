from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class TimeStampedModel(models.Model):
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeModified = models.DateTimeField(auto_now=True)

    # Abstract base class
    class Meta:
        abstract = True


class post(TimeStampedModel):
    # Leave this as 'name' b/c admin requires one
    name = models.CharField(default="", max_length=150)
    text = models.TextField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
                        # Allows us to access via user.posts
    PAGE_TYPE_CHOICES = (
        ('PRO', 'Problems'),
        ('IDE', 'Ideas'),
        ('QUE', 'Questions'),
        ('SIT', 'Site Feedback'),
    )
    page_type = models.CharField(max_length=3, choices=PAGE_TYPE_CHOICES)

    # Better string representation in admin and elsewhere
    def __unicode__(self):
        return self.name


class eduuser(AbstractUser):
    STUDENT = 'STU'
    TEACHER = 'TEA'
    PARENT = 'PAR'
    ADMINISTRATOR = 'ADM'
    OUTSIDER = 'OUT'

    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (PARENT, 'Parent'),
        (ADMINISTRATOR, 'Administrator'),
        (OUTSIDER, 'Outsider'),
    )

    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES)
