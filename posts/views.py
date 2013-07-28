# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from honeypot.decorators import check_honeypot
import datetime

from .forms import postForm
from .models import post, spam
from votes.models import vote

POSTS_ALLOWED_PER_DAY = 5

def home_page(request):
    return render(request, 'home.html')

def faq_page(request):
    return render(request, 'FAQ.html')

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
    if request.session.get('bad_form'):
        form = postForm(request.session.get('bad_form'))
        form.is_valid()
        del request.session['bad_form']
    else:
        form = postForm

    posts_all = post.objects.all().filter(page_type=page_type)
    # Sort logic
    sort_categs = ['Most Recent', 'Highest Rated', 'Most Votes']
    if sort_id=='1':
        sort_id = 1 #Keep as int
        posts_all = posts_all.order_by('-time_created')
    elif sort_id=='2':
        sort_id = 2
        posts_all = posts_all.order_by('-vote_percentage')
    elif sort_id=='3':
        sort_id = 3
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
        
        
    # Filling vote values
    vote_dict = {}
    # Grabs the current post and switches to its inner dictionary
    for current_post in posts:
        vote_dict[current_post] = {}
        user_dict = vote_dict[current_post]
        post_votes_by_user_type_helper(user_dict, current_post)

    # Display number of posts left for the day
    if request.user.is_authenticated():
        posts_in_last_24_hours = post.objects.all().filter(
            time_created__gte=datetime.datetime.now()-datetime.timedelta(hours=24),
            user_id=request.user
        )
        posts_left = POSTS_ALLOWED_PER_DAY - posts_in_last_24_hours.count()
    else:
        posts_left = None
    
    return render(request, 'base_post.html',
                  {'posts': posts, 'form': form, 'vote_dict': vote_dict,
                   'page_title': page_title, 'page_abbrev': page_type,
                   'current_page': current_page,
                   'user_color_dict': get_user_model().COLORS,
                   'sort_categs': sort_categs, 'sort_id':sort_id,
                   'posts_left': posts_left, 'page': page})

def user_page(request, user):
    """
    Displays a page with info about a certain user
    """
    user_of_interest = get_object_or_404(get_user_model(), username=user)
    user_posts = user_of_interest.posts.all()
    return render(request, 'user_page.html',
                  {'user_object': user_of_interest, 'user_posts': user_posts})

def post_page(request, post_id):
    """
    Displays a page with info about a certain post
    """
    post_of_interest = get_object_or_404(post, id=post_id)
    # Filling vote values
    user_dict = {}
    post_votes_by_user_type_helper(user_dict, post_of_interest)
    return render(request, 'post_page.html',
                  {'post': post_of_interest,
                   'user_color_dict': get_user_model().COLORS,
                   'user_dict': user_dict})

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
        posts_in_last_24_hours = post.objects.all().filter(
            time_created__gte=datetime.datetime.now()-datetime.timedelta(hours=24),
            user_id=request.user
        )
        if posts_in_last_24_hours.count() >= POSTS_ALLOWED_PER_DAY:
            return redirect(request.GET['next'])

    if request.POST:
        form = postForm(request.POST, instance=post_of_interest)
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
                request.session['bad_form'] = request.POST
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            # Should never be entered, but remove session if so
            del request.session['bad_form']
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
def mark_as_spam(request, id):
    post_of_interest = get_object_or_404(post, pk=id)
    spam_of_interest, bool_created = spam.objects.get_or_create(
        post_id = post_of_interest,
        user_id = request.user,
        )
    if bool_created == True:
        post_of_interest.check_spam_count()
    return redirect(request.GET['next'])


## Helper functions
def post_votes_by_user_type_helper(user_dict, post_of_interest):
    # For a given post, fills a dictionary with % up votes by user type
    post_votes = vote.objects.all().filter(post_id=post_of_interest)
    for user_type in get_user_model().USER_TYPE_CHOICES:
        all_votes = post_votes.filter(user_id__user_type=user_type[0])
        up_votes = all_votes.filter(vote_choice = vote.VOTE_CHOICES.upvote)
        if len(all_votes)==0:
            user_dict[user_type[0]] = 0
        else:
            user_dict[user_type[0]] = round(
                float(len(up_votes))/len(all_votes), 3
            )


    
