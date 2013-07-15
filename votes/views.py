from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import vote
from posts.models import post


@login_required
def up_vote(request, id):
    post_of_interest = post.objects.get(id=id)
    vote_of_interest, bool_created = vote.objects.get_or_create(
                post_id = post_of_interest,
                user_id = request.user,
                )
    # Scenario 1: Vote is being created. Default is up-vote so no need to save
    if bool_created == True:
        up_vote_to_add = 1
        total_vote_to_add = 1
    else:
        # Scenario 2: Vote is not being modified
        if vote_of_interest.vote_choice == vote.VOTE_CHOICES.upvote:
            return redirect(request.GET['next'])
        # Scenario 3: Vote is being switched
        else:
            up_vote_to_add = 1
            total_vote_to_add = 0
            vote_of_interest.vote_choice = vote.VOTE_CHOICES.upvote
            vote_of_interest.save()
    post_of_interest.update_votes(up_vote_to_add, total_vote_to_add)
    post_user = post_of_interest.user_id
    post_user.update_votes(up_vote_to_add, total_vote_to_add)
    return redirect(request.GET['next'])

@login_required
def down_vote(request, id):
    post_of_interest = post.objects.get(id=id)
    vote_of_interest, bool_created = vote.objects.get_or_create(
                post_id = post_of_interest,
                user_id = request.user,
                )
    # Scenario 1: Vote is being created. Default is up-vote so no need to save
    if bool_created == True:
        up_vote_to_add = 0
        total_vote_to_add = 1
        vote_of_interest.vote_choice = vote.VOTE_CHOICES.downvote
        vote_of_interest.save()
    else:
        # Scenario 2: Vote is not being modified
        if vote_of_interest.vote_choice == vote.VOTE_CHOICES.downvote:
            return redirect(request.GET['next'])
        # Scenario 3: Vote is being switched
        else:
            up_vote_to_add = -1
            total_vote_to_add = 0
            vote_of_interest.vote_choice = vote.VOTE_CHOICES.downvote
            vote_of_interest.save()
    post_of_interest.update_votes(up_vote_to_add, total_vote_to_add)
    post_user = post_of_interest.user_id
    post_user.update_votes(up_vote_to_add, total_vote_to_add)
    return redirect(request.GET['next'])
