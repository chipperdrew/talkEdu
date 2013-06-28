from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.backends.default.views import RegistrationView
from posts.forms import CustomRegistrationForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'posts.views.home_page', name='home'),
    url(r'^problems/$', 'posts.views.problems_page', name='problems'),
    # Called if error on login. MAY WANT TO CHANGE TEMPLATE???
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'base.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^user/(?P<user>[-\w]+)/$', 'posts.views.user_page',
        name='user_page'),

    # Django-registration package
    url(r'^accounts/register/$', RegistrationView.as_view(
        form_class=CustomRegistrationForm)),
    url(r'^accounts/', include('registration.backends.default.urls'),
        name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
)
