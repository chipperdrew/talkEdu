from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render
from model_utils import Choices

MAX_AKISMET = 3

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
        (OUTSIDER, 'Other'),
    )
#    COLORS = {STUDENT: "#405952", TEACHER: "#F54F29", PARENT: "#9C9B7A",
#              ADMINISTRATOR: "#FFD393", OUTSIDER: "#FF974F"}
    COLORS = {STUDENT: "Red", TEACHER: "Green", PARENT: "Blue",
              ADMINISTRATOR: "Orange", OUTSIDER: "Purple"}

    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES,
                                 default=STUDENT)
    up_votes = models.SmallIntegerField(default=0)
    total_votes = models.SmallIntegerField(default=0)
    # AC: 7/14/13 Consider setting min/max on float field
    vote_percentage = models.FloatField(default=0)
    akismet_hits = models.SmallIntegerField(default=0)

    def update_votes(self, up_vote_to_add, total_vote_to_add):
        from votes.models import vote #Must import here b/c cross-relationship
        self.up_votes = self.up_votes + up_vote_to_add
        self.total_votes = self.total_votes + total_vote_to_add
        if self.total_votes != 0:
            self.vote_percentage = round(float(self.up_votes)/self.total_votes, 3)
            self.save()

    def check_akismet(self, request):
        self.akismet_hits += 1
        ban = False
        if self.akismet_hits >= MAX_AKISMET:
            self.is_active = False #Cannot login AND middleware forces logout
            ban = True
        self.save()
        return render(request, 'caught_spam.html',
                          {'max_spam': MAX_AKISMET, 'ban': ban})
