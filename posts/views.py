from django.shortcuts import render, redirect
from posts.models import Post

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def problems_page(request):
    if request.method == 'POST':
       Post.objects.create(text = request.POST['post_content'])
    # posts is created so we can iterate over it to display all posts in template
    posts = Post.objects.all()
    return render(request, 'problems.html', {'posts': posts})
