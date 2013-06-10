from django.shortcuts import render
from posts.models import Post

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def problems_page(request):
    post = Post.objects.create(text = request.POST.get('post_content', ''))
    return render(request, 'problems.html', {
        'post_content_display': request.POST.get('post_content', ''),
        })
