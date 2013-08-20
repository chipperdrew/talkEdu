# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
import datetime
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from honeypot.decorators import check_honeypot
from raven.contrib.django.models import client

from posts.forms import postForm
from posts.models import post
from votes.models import vote, spam
from comments.forms import commentForm
from comments.models import comment
from comments.views import spam_check

POSTS_ALLOWED_PER_DAY = 5

def home_page(request):
#    try:
#        1 / 0
#    except Exception:
#        client.captureException()
    return render(request, 'home.html')

def faq_page(request):
    return render(request, 'FAQ.html')

def learn_more(request):
    return render(request, 'learn_more.html',
                  {'user_color_dict': get_user_model().COLORS,
                   'user_type_dict': get_user_model().USER_TYPE_CHOICES,
                   'page_type_dict': post.PAGE_TYPE_CHOICES
                   })

def display_page_helper(request, page, sort_id=1):
    """
    Helper function to display any pages with posts.
    Paginator logic adapted from:
    https://docs.djangoproject.com/en/dev/topics/pagination/
    """
    current_page = page #Save current page and pass it to template
    page_title = page.title()
    if page_title == 'Problems':
        page_type = post.PROBLEMS
    elif page_title == 'Ideas':
        page_type = post.IDEAS
    elif page_title == 'Questions':
        page_type = post.QUESTIONS
    elif page_title == 'Site_Feedback':
        page_title = 'Site Feedback'
        page_type = post.SITE_FEEDBACK
    else:
        return Http404
    
    # If given a bad form, show form and errors
    if request.session.get('bad_post_form'):
        form = postForm(request.session.get('bad_post_form'))
        form.is_valid()
        del request.session['bad_post_form']
    else:
        form = postForm

    posts_all = post.objects.filter(page_type=page_type)
    # Sort logic - Default is Most Recent
    sort_categs = ['Most Recent', 'Highest Rated', 'Most Votes']
    sort_id = int(sort_id) #Keep as int
    if sort_id==2:
        posts_all = posts_all.order_by('-vote_percentage')
    elif sort_id==3:
        posts_all = posts_all.order_by('-total_votes')
    else:
        pass
    
    # Paginator logic
    paginator = Paginator(posts_all, 5)
    page = request.GET.get('page')
    if page is None:
        page = 1
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    
    # Display number of posts left for the day
    if request.user.is_authenticated():
        posts_in_last_24_hours = post.objects.filter(
            time_created__gte=datetime.datetime.now()-datetime.timedelta(hours=24),
            user_id=request.user
        )
        posts_left = POSTS_ALLOWED_PER_DAY - posts_in_last_24_hours.count()
    else:
        posts_left = None
    
    return render(request, 'base_post.html',
                  {'posts': posts, 'form': form, 'posts_left': posts_left,
                   'page_title': page_title, 'page_abbrev': page_type,
                   'current_page': current_page, 'page': page,
                   'user_color_dict': get_user_model().COLORS,
                   'sort_categs': sort_categs, 'sort_id':sort_id #For green checkmark
                   })

def user_page(request, user):
    """
    Displays a page with info about a certain user
    """
    user_of_interest = get_object_or_404(get_user_model(), username=user)
    user_posts = user_of_interest.posts.all()[:10]
    user_comments = user_of_interest.comments.order_by('-time_created')[:10]
    return render(request, 'user_page.html',
                  {'user_object': user_of_interest,
                   'user_posts': user_posts, 'user_comments': user_comments})

def post_page(request, post_id):
    """
    Displays a page with info about a certain post & a comment section
    """
    post_of_interest = get_object_or_404(post, id=post_id)
    # If given a bad comment form, show form and errors
    if request.session.get('bad_comment_form'):
        comment_form = commentForm(request.session.get('bad_comment_form'))
        comment_form.is_valid()
        del request.session['bad_comment_form']
    else:
        comment_form = commentForm
        
    # Determine which comments to show
    post_comments = comment.objects.filter(post_id=post_id)
    num_comments = len(post_comments)
    if 'all' not in request.path:
        post_comments = post_comments.filter(depth=0)
        
    return render(request, 'post_page.html',
                  {'post': post_of_interest, 'num_comments': num_comments,
                   'user_color_dict': get_user_model().COLORS,
                   'comment_form': comment_form, 'comment_tree': post_comments,
                   })

###### POST VIEWS #######
@check_honeypot
def edit(request, id=None, page_abbrev=None):
    """
    Called when making a new 'post' or editing an existing 'post'.
    Adapted from: http://stackoverflow.com/questions/1854237/django-edit-form-based-on-add-form
    """
    ## Preferred over @login_required b/c login_required doesn't save POST
    ## requests, thus causing an error upon return to POST page
    if not request.user.is_authenticated():
        return redirect(reverse('accounts.views.login'))
    
    if id:
        post_of_interest = get_object_or_404(post, pk=id)
    # Create a new post if it doesn't already exist
    else:
        post_of_interest = post(user_id = request.user, page_type = page_abbrev)
        # Limit number of posts per 24 hours
        posts_in_last_24_hours = post.objects.filter(
            time_created__gte=datetime.datetime.now()-datetime.timedelta(hours=24),
            user_id=request.user
        )
        if posts_in_last_24_hours.count() >= POSTS_ALLOWED_PER_DAY:
            return redirect(request.GET['next'])

    if request.POST:
        form = postForm(request.POST, instance=post_of_interest)
        # SPAM CHECK
        content = form['title'].value() + form['text'].value()
#        bool_spam = spam_check(content, post_of_interest, request)
#        if bool_spam:
#            return request.user.check_akismet(request)
        if form.is_valid():
            form.save()
        else:
            # If error on edit, display error
            if 'edit' in request.path:
                return render(request, 'post_edit.html',
                              {'id': id, 'form': form,
                               'redirect_to':request.GET['next']})
            else:
                # For new post errors, display_page_helper needs access
                request.session['bad_post_form'] = request.POST
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            # Should never be entered, but remove session if so
            del request.session['bad_post_form']
            return redirect('/')
    else:
        form = postForm(instance=post_of_interest)
        return render(request, 'post_edit.html',
                      {'id': id, 'form': form,
                       'redirect_to':request.GET['next']}) #used by edit temp

@login_required
def delete(request, id):
    """
    Deletes a post, returns user to current page
    """
    post_of_interest = get_object_or_404(post, pk=id)
    if post_of_interest.user_id == request.user:
        post_of_interest.delete()
    else:
        raise PermissionDenied()
    return redirect(request.GET['next']) #provided by base_post template

@login_required
def post_mark_as_spam(request, id):
    if not request.is_ajax():
        raise Http404()
    post_of_interest = get_object_or_404(post, pk=id)
    spam_of_interest, bool_created = spam.objects.get_or_create(
        post_id = post_of_interest,
        user_id = request.user,
        )
    if bool_created:
        post_of_interest.check_spam_count()
        data = json.dumps({'id': id, 'item_type': 'p', })
        return HttpResponse(data, content_type='application/json')
    return HttpResponse()


