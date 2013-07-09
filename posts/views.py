# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import postForm
from .models import post


def home_page(request):
    return render(request, 'home.html')

def display_page_helper(request, page_type, template):
    """
    Helper function to display any pages with posts
    """
    posts = post.objects.all().filter(page_type=page_type)
    return render(request, template, {'posts': posts, 'form': postForm})

def problems_page(request):
    return display_page_helper(request, 'PRO', 'problems.html')

def ideas_page(request):
    return display_page_helper(request, 'IDE', 'ideas.html')

def questions_page(request):
    return display_page_helper(request, 'QUE', 'questions.html')

def site_feedback_page(request):
    return display_page_helper(request, 'SIT', 'site_feedback.html')

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


def edit(request, id=None):
    """
    Called when making a new 'post' or editing an existing 'post'.
    Adapted from: http://stackoverflow.com/questions/1854237/django-edit-form-based-on-add-form
    """
    # If id provided, find existing post
    if id:
        post_of_interest = get_object_or_404(post, pk=id)
    # Else - create a new post
    else:
        post_of_interest = post(
            user_id = request.user,
            page_type = str(request.GET['next'][1:4]).upper()
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

