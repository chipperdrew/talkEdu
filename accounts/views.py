from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404

# All of these used by CustomRegistrationView
from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite

    
def login(request, *args, **kwargs):
    """
    Adds remember me feature, then calls django's provided login view
    """
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)


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
