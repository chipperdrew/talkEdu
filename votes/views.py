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
    # Default vote choice is up_vote, so only modify vote if accessed via get
    if bool_created == False:
        vote_of_interest.vote_choice = vote.VOTE_CHOICES.upvote
        vote_of_interest.save()
    post_of_interest.update_vote_percentage()
    return redirect(request.GET['next'])

@login_required
def down_vote(request, id):
    post_of_interest = post.objects.get(id=id)
    vote_of_interest, bool_created = vote.objects.get_or_create(
                post_id = post_of_interest,
                user_id = request.user,
                )
    vote_of_interest.vote_choice = vote.VOTE_CHOICES.downvote
    vote_of_interest.save()
    post_of_interest.update_vote_percentage()
    return redirect(request.GET['next'])
