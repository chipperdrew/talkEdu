from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils import Choices

# Adapted from '2 Scoops of Django' book
class TimeStampedModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True,
                                        default=timezone.now())
    time_modified = models.DateTimeField(auto_now=True,
                                         default=timezone.now())

    # Abstract base class
    class Meta:
        abstract = True


class post(TimeStampedModel):
    # Leave this as 'name' b/c admin requires one
    title = models.CharField(default="", max_length=150)
    text = models.TextField(blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
                        # Allows us to access via user.posts

    # IF MODIFY BELOW, must change 'edit' view
    PROBLEMS = 'PRO'
    IDEAS = 'IDE'
    QUESTIONS = 'QUE'
    SITE_FEEDBACK = 'SIT'
    
    PAGE_TYPE_CHOICES = Choices(
        (PROBLEMS, 'Problems'),
        (IDEAS, 'Ideas'),
        (QUESTIONS, 'Questions'),
        (SITE_FEEDBACK, 'Site Feedback'),
    )
    page_type = models.CharField(max_length=3, choices=PAGE_TYPE_CHOICES)

    # Better string representation in admin and elsewhere
    def __unicode__(self):
        return self.title


class eduuser(AbstractUser):
    STUDENT = 'STU'
    TEACHER = 'TEA'
    PARENT = 'PAR'
    ADMINISTRATOR = 'ADM'
    OUTSIDER = 'OUT'

    USER_TYPE_CHOICES = Choices(
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (PARENT, 'Parent'),
        (ADMINISTRATOR, 'Administrator'),
        (OUTSIDER, 'Outsider'),
    )

    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES)
