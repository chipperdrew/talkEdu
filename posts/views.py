# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
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
                            timeModified = timezone.now())
    posts = Post.objects.all()
    return render(request, 'problems.html', {'posts': posts})

def login(request):
    return redirect('/')
