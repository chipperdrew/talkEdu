# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import postForm
from .models import post, vote


def home_page(request):
    return render(request, 'home.html')

def display_page_helper(request, page_type, template):
    """
    Helper function to display any pages with posts.
    Paginator logic adapted from:
    https://docs.djangoproject.com/en/dev/topics/pagination/
    """
    posts_all = post.objects.all().filter(page_type=page_type)
    paginator = Paginator(posts_all, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    vote_dict = {}
    # Grabs the current post and switches to its inner dictionary
    for current_post in posts:
        vote_dict[current_post] = {}
        post_votes = vote.objects.all().filter(
            post_id=current_post,
        )
        user_dict = vote_dict[current_post]
        # Gets the votes by user_type, then stores % of up_votes in inner dict
        for user_type in get_user_model().USER_TYPE_CHOICES:
            all_votes = post_votes.filter(user_id__user_type=user_type[0])
            up_votes = all_votes.filter(vote_choice = vote.VOTE_CHOICES.upvote)
            if len(all_votes)==0:
                user_dict[user_type[0]] = 0
            else:
                user_dict[user_type[0]] = round(
                    float(len(up_votes))/len(all_votes), 3
                )
    return render(request, template, {'posts': posts, 'form': postForm,
                                      'vote_dict': vote_dict})

def problems_page(request):
    return display_page_helper(request, post.PAGE_TYPE_CHOICES.PRO,
                               'problems.html')

def ideas_page(request):
    return display_page_helper(request, post.PAGE_TYPE_CHOICES.IDE,
                               'ideas.html')

def questions_page(request):
    return display_page_helper(request, post.PAGE_TYPE_CHOICES.QUE,
                               'questions.html')

def site_feedback_page(request):
    return display_page_helper(request, post.PAGE_TYPE_CHOICES.SIT,
                               'site_feedback.html')

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
    return render(request, 'post_page.html', {'post': post_of_interest})

###### POST VIEWS #######
def edit(request, id=None):
    """
    Called when making a new 'post' or editing an existing 'post'.
    Adapted from: http://stackoverflow.com/questions/1854237/django-edit-form-based-on-add-form
    """
    if id:
        post_of_interest = get_object_or_404(post, pk=id)
    # Create a new post if it doesn't already exist
    else:
        post_of_interest = post(
            user_id = request.user,
            page_type = str(request.GET['next'][1:4]).upper()
            #Modify above line if changes are made to PAGE_TYPE_CHOICES
            )

    if request.POST:
        form = postForm(request.POST, instance=post_of_interest)
        if form.is_valid():
            form.save()
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('/')
    else:
        form = postForm(instance=post_of_interest)
        return render(request, 'post_edit.html',
                      {'id': id, 'form': form,
                       'redirect_to':request.GET['next']}) #used by edit temp

def delete(request, id):
    """
    Deletes a post, returns user to current page
    """
    post_of_interest = get_object_or_404(post, pk=id)
    post_of_interest.delete()
    return redirect(request.GET['next']) #provided by base_post template


####### VOTING VIEWS ########
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
    return redirect(request.GET['next'])

def down_vote(request, id):
    post_of_interest = post.objects.get(id=id)
    vote_of_interest, bool_created = vote.objects.get_or_create(
                post_id = post_of_interest,
                user_id = request.user,
                )
    vote_of_interest.vote_choice = vote.VOTE_CHOICES.downvote
    vote_of_interest.save()
    return redirect(request.GET['next'])

