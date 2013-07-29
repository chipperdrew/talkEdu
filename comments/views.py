from django.shortcuts import render, redirect, get_object_or_404
from honeypot.decorators import check_honeypot

from .forms import commentForm
from .models import comment
from posts.models import post


@check_honeypot
def new_comment(request, post_id):
    """
    Based off of edit view in post app
    """
    ## Preferred over @login_required b/c login_required doesn't save POST
    ## requests, thus causing an error upon return to POST page
    if not request.user.is_authenticated():
        return redirect(reverse('accounts.views.login'))
    
    comment_of_interest = comment(user_id = request.user,
                                  post_id = post.objects.get(id=post_id))

    form = commentForm(request.POST, instance=comment_of_interest)
    if form.is_valid():
        form.save()
    else:
        # For new post errors, display_page_helper needs access
        request.session['bad_comment_form'] = request.POST
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        # Should never be entered, but remove session if so
        del request.session['bad_form']
        return redirect('/')
