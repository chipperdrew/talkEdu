from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from model_utils import Choices
from picklefield.fields import PickledObjectField
import datetime

from accounts.models import eduuser

POST_SPAM_LIMIT = 10

# Adapted from '2 Scoops of Django' book
class TimeStampedVoteableModel(models.Model):
    # Abstract base class
    class Meta:
        abstract = True
        ordering = ['-time_created']
        
    time_created = models.DateTimeField(db_index=True, auto_now_add=True,
                                        default=datetime.datetime.now())
    time_modified = models.DateTimeField(auto_now=True,
                                         default=datetime.datetime.now())
    up_votes = models.SmallIntegerField(default=0)
    total_votes = models.SmallIntegerField(db_index=True, default=0)
    vote_percentage = models.FloatField(db_index=True, default=0) ##Set min/max

    votes_by_user_type = PickledObjectField(
        default={eduuser.STUDENT: [0,0,0],
                 eduuser.TEACHER: [0,0,0],
                 eduuser.PARENT: [0,0,0],
                 eduuser.ADMINISTRATOR: [0,0,0],
                 eduuser.OUTSIDER: [0,0,0]
                })

    # Purpose - to see the number of spam counts in admin and reset if necessary
    spam_count = models.SmallIntegerField(default=0)

    def update_votes(self, up_vote_to_add, total_vote_to_add):
        from votes.models import vote #Must import here b/c cross-relationship
        self.up_votes += up_vote_to_add
        self.total_votes += total_vote_to_add
        if self.total_votes != 0:
            self.vote_percentage = round(float(self.up_votes)/self.total_votes, 3)
        self.save()


class post(TimeStampedVoteableModel):
    # Leave this as 'name' b/c admin requires one
    title = models.CharField(default="", max_length=150)
    text = models.TextField(blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
                                related_name='posts')
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
    
    page_type = models.CharField(db_index=True, max_length=3,
                                 choices=PAGE_TYPE_CHOICES)

    def check_spam_count(self):
        # Not set to self.spam.count() in case there is a need to reset spam_count
        self.spam_count = self.spam_count + 1
        if self.spam_count >= POST_SPAM_LIMIT:
            page_type_first_letter = self.page_type[0]
            setattr(self, 'page_type', 'SP' + page_type_first_letter)
        else:
            pass
        self.save()
            
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_page', kwargs={"post_id": self.id})
