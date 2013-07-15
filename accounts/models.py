from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices


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

    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES,
                                 default=STUDENT)
    up_votes = models.SmallIntegerField(default=0)
    total_votes = models.SmallIntegerField(default=0)
    # AC: 7/14/13 Consider setting min/max on float field
    vote_percentage = models.FloatField(default=0)

    def update_votes(self, up_vote_to_add, total_vote_to_add):
        from votes.models import vote #Must import here b/c cross-relationship
        self.up_votes = self.up_votes + up_vote_to_add
        self.total_votes = self.total_votes + total_vote_to_add
        if self.total_votes != 0:
            self.vote_percentage = round(float(self.up_votes)/self.total_votes, 3)
            self.save()
