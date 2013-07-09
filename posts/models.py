from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone


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
    PAGE_TYPE_CHOICES = (
        ('PRO', 'Problems'),  # IF MODIFIED, must change 'edit' view
        ('IDE', 'Ideas'),
        ('QUE', 'Questions'),
        ('SIT', 'Site Feedback'),
    )
    page_type = models.CharField(max_length=3, choices=PAGE_TYPE_CHOICES)

    # Better string representation in admin and elsewhere
    def __unicode__(self):
        return self.title


class vote(models.Model):
    post_id = models.OneToOneField(post, primary_key=True)

    stu_up = models.IntegerField(default=0)
    tea_up = models.IntegerField(default=0)
    par_up = models.IntegerField(default=0)
    adm_up = models.IntegerField(default=0)
    out_up = models.IntegerField(default=0)

    stu_votes = models.IntegerField(default=0)
    tea_votes = models.IntegerField(default=0)
    par_votes = models.IntegerField(default=0)
    adm_votes = models.IntegerField(default=0)
    out_votes = models.IntegerField(default=0)

    def perc(self):
        if self.stu_votes==0:
            return 0
        else:
            return round(self.stu_up/float(self.stu_votes), 3) #Prevent int div


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


