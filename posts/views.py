# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .forms import postForm
from .models import post


def home_page(request):
    return render(request, 'home.html')

def display_page_helper(request, page_type, template):
    """
    Helper function to display any pages with posts
    """
    request.session['page_type'] = page_type # Used by 'edit' view for new posts
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
        post_of_interest = post(user_id=request.user,
                                page_type = request.session.get('page_type'))

    if request.POST:
        form = postForm(request.POST, instance=post_of_interest)
        if form.is_valid():
            form.save()
            # This logic is TERRIBLE. Refactor when smarter :)
            if request.session.get('page_type')=='PRO':
                return redirect('/problems/')
            elif request.session.get('page_type')=='IDE':
                return redirect('/ideas/')
            elif request.session.get('page_type')=='QUE':
                return redirect('/questions/')
            else:
                return redirect('/site_feedback/')
    else:
        form = postForm(instance=post_of_interest)
        return render(request, 'post_edit.html', {'id': id, 'form': form})

def delete(request, id):
    post_of_interest = get_object_or_404(post, pk=id)
    post_of_interest.delete()
    # This logic is TERRIBLE. Refactor when smarter :)
    if request.session.get('page_type')=='PRO':
        return redirect('/problems/')
    elif request.session.get('page_type')=='IDE':
        return redirect('/ideas/')
    elif request.session.get('page_type')=='QUE':
        return redirect('/questions/')
    else:
        return redirect('/site_feedback/')

