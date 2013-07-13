from django.conf import settings
from django.core.urlresolvers import reverse
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

    def get_vote_percentage(self):
        from votes.models import vote #Must import here b/c cross-relationship
        all_votes = self.votes.all().count()
        if all_votes==0:
            return 0
        else:
            up_votes = self.votes.filter(vote_choice = vote.VOTE_CHOICES.upvote).count()
            return round(float(up_votes)/all_votes, 3)
    
    # Better string representation in admin and elsewhere
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_page', kwargs={"post_id": self.id}) 
