from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import eduuserForm
    
def login(request, *args, **kwargs):
    """
    Adds remember me feature, then calls django's provided login view
    """
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        if not request.POST.get('username', None):
            request.method = 'GET' #Prevents lockout on accidental submit
    return auth_views.login(request, *args, **kwargs)

@login_required
def user_type_change(request):
    return render(request, 'user_type_change_form.html', {'form': eduuserForm})

def user_type_change_done(request, id):
    user_of_interest = get_object_or_404(get_user_model(), id=id)
    old_type = user_of_interest.user_type
    
    # Prevent uncalled for changes
    if request.user != user_of_interest:
        return redirect('/')
    form = eduuserForm(request.POST, instance=user_of_interest)
    if form.is_valid():
        form.save()
        
        # Update ALL of the post/comment vote tallies to reflect change
        new_type = form['user_type'].value()
        for vote in user_of_interest.votes.all():
            if vote.post_id:
                id = vote.post_id
            else:
                id = vote.comment_id
            id.votes_by_user_type[old_type][1] -= 1
            id.votes_by_user_type[new_type][1] += 1
            if vote.vote_choice=='upvote':
                id.votes_by_user_type[old_type][0] -= 1
                id.votes_by_user_type[new_type][0] += 1
            # Update percentages
            if id.votes_by_user_type[old_type][1] > 0:
                id.votes_by_user_type[old_type][2] = round(float(id.votes_by_user_type[old_type][0]) / id.votes_by_user_type[old_type][1], 3)
            else:
                id.votes_by_user_type[old_type][2] = 0
            id.votes_by_user_type[new_type][2] = round(float(id.votes_by_user_type[new_type][0]) / id.votes_by_user_type[new_type][1], 3)
            id.save()
        return render(request, 'user_type_change_done.html')
    else:
        # I don't know how this is possible, but just in case...
        return HttpResponse('Invalid change, please try again.')
