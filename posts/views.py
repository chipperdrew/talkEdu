
# USE FOR PRESENTATION LOGIC, NOT BUSINESS LOGIC (put that in models)
# from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from .models import post, eduuser

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def post_helper(request, page_type):
    if request.method == 'POST':
        post.objects.create(title = request.POST['post_title'],
                            text = request.POST['post_content'],
                            user_id = request.user,
                            page_type = page_type
                            )
    return post.objects.all().filter(page_type=page_type)
    
def problems_page(request):
    # posts is created so we can iterate over it to display all posts
    # in template
    posts = post_helper(request, 'PRO')
    return render(request, 'problems.html', {'posts': posts})

def ideas_page(request):
    posts = post_helper(request, 'IDE')
    return render(request, 'ideas.html', {'posts': posts})

def questions_page(request):
    posts = post_helper(request, 'QUE')
    return render(request, 'questions.html', {'posts': posts})

def site_feedback_page(request):
    posts = post_helper(request, 'SIT')
    return render(request, 'site_feedback.html', {'posts': posts})

def login(request, *args, **kwargs):
    # Adds remember me feature
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)

def user_page(request, user):
    # Currently is cAsE sEnSiTiVe
    # user=user.lower()
    user_object = eduuser.objects.get(username=user)
    user_posts = user_object.posts.all()
    return render(request, 'user_page.html',
                  {'user_object': user_object, 'user_posts': user_posts})

def post_page(request, post_id):
    post_object = post.objects.get(id=post_id)
    return render(request, 'post_page.html', {'post_object': post_object})


class CustomRegistrationView(RegistrationView):
    """
    Needed override this django-registration feature to have it create
    a profile with extra field
    """
    def register(self, request, **cleaned_data):
        username, email, password, user_type = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1'], cleaned_data['user_type']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, user_type, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
