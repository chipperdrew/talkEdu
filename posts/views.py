# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def problems_page(request):
    # posts is created so we can iterate over it to display all posts
    # in template
    if request.method == 'POST':
        Post.objects.create(text = request.POST['post_content'],
                            timeCreated = timezone.now(),
                            timeModified = timezone.now(),
                            user_id = request.user)
    posts = Post.objects.all()
    return render(request, 'problems.html', {'posts': posts})

def user_page(request, user):
    # Currently is cAsE sEnSiTiVe
    # user=user.lower()
    user_object = User.objects.get(username=user)
    user_posts = user_object.posts.all()
    return render(request, 'user_page.html',
                  {'user_object': user_object, 'user_posts': user_posts})
