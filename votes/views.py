from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from .models import vote
from posts.models import post
from comments.models import comment


@login_required
def up_vote(request, id, item_type):
    item_of_interest, vote_of_interest, bool_created = check_type_helper(
        request, id, item_type
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
    update_stats_helper(item_type, item_of_interest, up_vote_to_add,
                        total_vote_to_add, request.user.user_type)
    return redirect(request.GET['next'])

@login_required
def down_vote(request, id, item_type):
    item_of_interest, vote_of_interest, bool_created = check_type_helper(
        request, id, item_type
    )
    # Scenario 1: Vote is being created.
    if bool_created == True:
        up_vote_to_add = 0
        total_vote_to_add = 1
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
    update_stats_helper(item_type, item_of_interest, up_vote_to_add,
                        total_vote_to_add, request.user.user_type)
    return redirect(request.GET['next'])

def check_type_helper(request, id, item_type):
    """
    Uses provided type to determine if post or comment
    """
    if item_type=='p':
        item_of_interest = post.objects.get(id=id)
        vote_of_interest, bool_created = vote.objects.get_or_create(
            post_id = item_of_interest,
            user_id = request.user,
        )
    elif item_type=='c':
        item_of_interest = comment.objects.get(id=id)
        vote_of_interest, bool_created = vote.objects.get_or_create(
            comment_id = item_of_interest,
            user_id = request.user,
        )
    else:
        return Http404()
    return item_of_interest, vote_of_interest, bool_created

def update_stats_helper(item_type, item_of_interest, up_vote_to_add,
                        total_vote_to_add, user_type):
    # Update the post/comment overall count
    item_of_interest.update_votes(up_vote_to_add, total_vote_to_add)
    # If post, update the user overall count
    if item_type=='p':
        post_user = item_of_interest.user_id
        post_user.update_votes(up_vote_to_add, total_vote_to_add)

    # Update the specific user_type vote dict in post/comment
    item_of_interest.votes_by_user_type[user_type][0] += up_vote_to_add
    item_of_interest.votes_by_user_type[user_type][1] += total_vote_to_add
    if item_of_interest.votes_by_user_type[user_type][1] > 0:
        item_of_interest.votes_by_user_type[user_type][2] = round(float(
            item_of_interest.votes_by_user_type[user_type][0])/item_of_interest.votes_by_user_type[user_type][1], 3)
    item_of_interest.save()
