from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from honeypot.decorators import check_honeypot
from itertools import ifilter

from .forms import commentForm
from .models import comment, spam
from posts.models import post

@check_honeypot
def new_comment(request, post_id):
    """
    Posts a new comment
    """
    # Would use @login_required but can't handle POST request on return
    if not request.user.is_authenticated():
        return redirect(reverse('accounts.views.login'))
    
    comment_of_interest = comment(user_id = request.user,
                                  post_id = post.objects.get(id=post_id))
    form = commentForm(request.POST, instance=comment_of_interest)
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            parent = form['parent'].value()
            if parent == '':
                #Set a blank path then save it to get an ID
                temp.path = []
                temp.save()
                temp.path = [temp.id]
            else:
                #Get the parent node
                node = comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path
                #Store parents path then apply comment ID
                temp.save()
                temp.path.append(temp.id)
                
            #Final save for parents and children
            temp.save()
        else:
            # Comment errors -- store in session for post_page view
            request.session['bad_comment_form'] = request.POST
            
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        # Should never be entered, but remove session if so
        del request.session['bad_comment_form']
        return redirect('/')


@login_required
def delete_comment(request, comment_id):
    comment_of_interest = get_object_or_404(comment, pk=comment_id)
    if comment_of_interest.user_id == request.user:
        delete_comment_path_helper(comment_of_interest)
    else:
        raise PermissionDenied()
    return redirect(request.GET['next'])

@login_required
def comment_mark_as_spam(request, id):
    """
    Based off of post view, but checks the boolean returned by check_spam_count
    b/c needs to delete comment AND children
    """
    comment_of_interest = get_object_or_404(comment, pk=id)
    spam_of_interest, bool_created = spam.objects.get_or_create(
        comment_id = comment_of_interest,
        user_id = request.user,
        )
    if bool_created:
        bool_spam_limit = comment_of_interest.check_spam_count()
        if bool_spam_limit:
            delete_comment_path_helper(comment_of_interest)
    return redirect(request.GET['next'])

def delete_comment_path_helper(comment_of_interest):
    # Need to remove children of post (sounds evil)
    post_comments = comment.objects.all().filter(post_id=comment_of_interest.post_id)
    for com in post_comments:
        if comment_of_interest.id in com.path:
            com.delete()
    # And remove initial comment
    comment_of_interest.delete()
