import akismet
import datetime
import json
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import loader, RequestContext
from honeypot.decorators import check_honeypot
from itertools import ifilter

from comments.forms import commentForm
from comments.models import comment
from posts.models import post
from votes.models import spam

COMMENT_TIME_FRAME = 15 #Time, in seconds, that must elapse between comments

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
        # SPAM CHECK
#        bool_spam = spam_check(form['content'].value(), comment_of_interest, request)
#        if bool_spam:
#            return request.user.check_akismet(request)

        # Check for too frequent commenting (likely spam)
        comments_in_last_min = comment.objects.filter(
            time_created__gte=datetime.datetime.now()-datetime.timedelta(seconds=COMMENT_TIME_FRAME),
            user_id=request.user
        )
        if len(comments_in_last_min)>=1:
            return render(request, 'rapid_comment.html',
                          {'time_frame': COMMENT_TIME_FRAME,
                           'redirect_to': request.GET['next'],
                           'content': form['content'].value()}
                          )

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
                node.children += 1 #Keep track of children to display
                node.save()
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
    if not request.is_ajax():
        raise Http404()
    comment_of_interest = get_object_or_404(comment, pk=id)
    spam_of_interest, bool_created = spam.objects.get_or_create(
        comment_id = comment_of_interest,
        user_id = request.user,
        )
    if bool_created:
        bool_spam_limit = comment_of_interest.check_spam_count()
        if bool_spam_limit:
            delete_comment_path_helper(comment_of_interest)
        data = json.dumps({'id': id, 'item_type': 'c', })
        return HttpResponse(data, content_type='application/json')
    return HttpResponse()
    
def show_replies(request, comment_id):
    if not request.is_ajax():
        raise Http404()
    comment_of_interest = comment.objects.get(id=comment_id)
    depth = comment_of_interest.depth
    post_comments = comment.objects.filter(post_id=comment_of_interest.post_id)
    comments_array = []
    for com in post_comments:
        if com.depth <= depth:
            comments_array.append(com)
        if comment_of_interest.id in com.path and com.depth==depth+1:
            comments_array.append(com)
    return render_to_response(
        'comment_display.html', {'comment_tree': comments_array, 'user_color_dict': get_user_model().COLORS},
        context_instance=RequestContext(request)
    )
    #data = serializers.serialize('json', {'comment_tree': comments_array})
    #return HttpResponse(data, content_type='application/json')


# Helper Functions
def delete_comment_path_helper(comment_of_interest):
    # Need to remove children of post (sounds evil)
    post_comments = comment.objects.filter(post_id=comment_of_interest.post_id)
    for com in post_comments:
        if comment_of_interest.id in com.path:
            com.delete()
    # Decrement parent count of children
    if comment_of_interest.depth != 0:
        comment_path = comment_of_interest.path
        del comment_path[-1]
        parent = comment.objects.get(path=comment_path)
        parent.children -= 1
        parent.save()
    # And remove initial comment
    comment_of_interest.delete()

def spam_check(content, item_of_interest, request):
    """
    Uses AKISMET to check if comment is spam
    """
    akismet.USERAGENT = "David Lynch's Python library/1.0"
    my_api_key = settings.AKISMET_KEY

    try:
        real_key = akismet.verify_key(my_api_key,"http://www.YouTalkEdu.com")
        if real_key:
            is_spam = akismet.comment_check(
                my_api_key,"http://www.YouTalkEdu.com",request.META['REMOTE_ADDR'],
                request.META['HTTP_USER_AGENT'],
                request.META.get('HTTP_REFERER', ''),
                comment_content=content,
                comment_auther_email=item_of_interest.user_id.email)
            if is_spam:
                return True
            else:
                return False
    except akismet.AkismetError, e:
        print 'Something went wrong, allowing comment'
        print e.response, e.statuscode
        return False
