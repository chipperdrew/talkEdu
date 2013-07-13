from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# All of these used by CustomRegistrationView
from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite

from .forms import eduuserForm
    
def login(request, *args, **kwargs):
    """
    Adds remember me feature, then calls django's provided login view
    """
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)

@login_required
def user_type_change(request):
    return render(request, 'user_type_change_form.html', {'form': eduuserForm})

def user_type_change_done(request, id):
    user_of_interest = get_object_or_404(get_user_model(), id=id)
    
    # Prevent uncalled for changes
    if request.user != user_of_interest:
        return redirect('/')
    form = eduuserForm(request.POST, instance=user_of_interest)
    if form.is_valid():
        form.save()
        return render(request, 'user_type_change_done.html')
    else:
        # I don't know how this is possible, but just in case...
        return HttpResponse('Invalid change, please try again.')

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
