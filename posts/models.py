from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils import Choices


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




class vote(models.Model):

    VOTE_CHOICES = Choices(
        ('upvote'),
        ('downvote'),
    )

    post_id = models.ForeignKey(post, primary_key=True)
    user_id = models.ForeignKey(eduuser)
    vote_choice = models.CharField(max_length=8, choices=VOTE_CHOICES,
                                   default=VOTE_CHOICES.upvote)
"""
class vote(models.Model):
    post_id = models.OneToOneField(post, primary_key=True)

    vote_dict = {} #Names of fields are stored as vote_dict
    for user_type in getattr(eduuser, 'USER_TYPE_CHOICES'):
        models.IntegerField(
            default=0, name=user_type[0]+'_up')
        models.IntegerField(
            default=0, name=user_type[0]+'_votes')
    
    a = models.IntegerField(
        default=0, name=getattr(eduuser, 'STUDENT')+'_up')
    b = models.IntegerField(
        default=0, name=getattr(eduuser, 'TEACHER')+'_up')
    c = models.IntegerField(
        default=0, name=getattr(eduuser, 'PARENT')+'_up')
    d = models.IntegerField(
        default=0, name=getattr(eduuser, 'ADMINISTRATOR')+'_up')
    e = models.IntegerField(
        default=0, name=getattr(eduuser, 'OUTSIDER')+'_up')
    
    models.IntegerField(
        default=0, name=getattr(eduuser, 'STUDENT')+'_votes')
    models.IntegerField(
        default=0, name=getattr(eduuser, 'TEACHER')+'_votes')
    models.IntegerField(
        default=0, name=getattr(eduuser, 'PARENT')+'_votes')
    models.IntegerField(
        default=0, name=getattr(eduuser, 'ADMINISTRATOR')+'_votes')
    models.IntegerField(
        default=0, name=getattr(eduuser, 'OUTSIDER')+'_votes')

    def perc(self):
        perc_array = []
        for user_type in getattr(eduuser, 'USER_TYPE_CHOICES'):
            up = float(getattr(self, user_type[0]+'_up')) #Prevent int divis
            votes = getattr(self, user_type[0]+'_votes')
            if votes==0:
                perc_array.append(0)
            else:
                perc_array.append(round(up/votes, 3))
        return perc_array
"""
